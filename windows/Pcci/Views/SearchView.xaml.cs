using System;
using System.ComponentModel;
using Microsoft.UI.Xaml;
using Microsoft.UI.Xaml.Controls;
using Microsoft.UI.Xaml.Input;
using Pcci.Models;
using Pcci.ViewModels;
using Windows.ApplicationModel.DataTransfer;
using Windows.System;

namespace Pcci;

/// <summary>
/// Finding a song online, and the results it found.
///
/// The list and the notes are bound to the state's own collections, so a search that
/// comes back while the user is looking elsewhere still lands. Everything else is
/// updated in one place, from one method, the way the rest of this app does it.
/// </summary>
public sealed partial class SearchView : UserControl
{
    private AppState? _state;

    public SearchView() => InitializeComponent();

    public void Initialise(AppState state)
    {
        _state = state;
        ResultsList.ItemsSource = state.SearchResults;
        NotesList.ItemsSource = state.SearchNotes;
        state.SearchResults.CollectionChanged += (_, _) => Refresh();
        state.SearchNotes.CollectionChanged += (_, _) => Refresh();
        state.PropertyChanged += OnStateChanged;
        Refresh();
    }

    private void OnStateChanged(object? sender, PropertyChangedEventArgs args)
    {
        if (args.PropertyName is nameof(AppState.IsSearching) or nameof(AppState.SearchedFor)
            or nameof(AppState.IsBusy) or nameof(AppState.SearchQuery))
        {
            Refresh();
        }
    }

    private void Refresh()
    {
        if (_state is null) return;

        if (QueryBox.Text != _state.SearchQuery) QueryBox.Text = _state.SearchQuery;

        var searching = _state.IsSearching;
        var hasResults = _state.SearchResults.Count > 0;

        SearchingRow.Visibility = searching ? Visibility.Visible : Visibility.Collapsed;
        ResultsList.Visibility = hasResults && !searching ? Visibility.Visible : Visibility.Collapsed;
        NotesList.Visibility = _state.SearchNotes.Count > 0 ? Visibility.Visible : Visibility.Collapsed;

        var nothingFound = !searching && !hasResults && _state.SearchedFor is { } query;
        EmptyText.Visibility = nothingFound ? Visibility.Visible : Visibility.Collapsed;
        if (nothingFound) EmptyText.Text = $"Nothing came back for “{_state.SearchedFor}”.";

        SearchButton.IsEnabled = _state.SearchQuery.Trim().Length > 0 && !searching;
        PasteButton.IsEnabled = !_state.IsBusy;
    }

    private void OnQueryChanged(object sender, TextChangedEventArgs args)
    {
        if (_state is not null) _state.SearchQuery = QueryBox.Text;
    }

    private async void OnQueryKeyDown(object sender, KeyRoutedEventArgs args)
    {
        if (args.Key != VirtualKey.Enter || _state is null) return;
        args.Handled = true;
        await _state.SearchAsync();
    }

    private async void OnSearch(object sender, RoutedEventArgs args)
    {
        if (_state is not null) await _state.SearchAsync();
    }

    private async void OnImport(object sender, RoutedEventArgs args)
    {
        if (_state is null) return;
        if ((sender as FrameworkElement)?.Tag is SongMatch match)
        {
            await _state.ImportMatchAsync(match);
        }
    }

    /// <summary>
    /// Read the clipboard here rather than in the view model.
    ///
    /// The clipboard is a window's business, not the application state's, and reaching
    /// for it needs the UI thread. The state only ever sees the text.
    /// </summary>
    private async void OnPaste(object sender, RoutedEventArgs args)
    {
        if (_state is null) return;
        var text = "";
        try
        {
            var content = Clipboard.GetContent();
            if (content.Contains(StandardDataFormats.Text))
            {
                text = await content.GetTextAsync();
            }
        }
        catch (Exception)
        {
            // Another application can be holding the clipboard open. That is the same
            // situation as an empty one as far as anybody here is concerned.
            text = "";
        }
        await _state.ImportPastedAsync(text);
    }
}
