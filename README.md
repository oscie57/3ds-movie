# 3ds-movie

Web interface to watch movies/TV via a Jellyfin/similar server.

## Why?

I wanted to watch my movies from my PC on my 3DS to watch in bed or away from my computer, and I couldn't access Jellyfin on it. I got bored and thought, why not make my own interface? After just over an hour of development, I got a base working, albeit without TV working.

## Setup

You need Flask and that's basically it.

## `list.json`

The JSON has to be formatted like this:

```json
{
    "lists": {
        "LIST_NAME": {
            "title": "LIST_TITLE",
            "description": "LIST_DESCRIPTION",
            "folder": "LIST_LOCATION",
            "type": "LIST_TYPE"
        },
    }
}
```

Valid types are `tv` and `movie`.
