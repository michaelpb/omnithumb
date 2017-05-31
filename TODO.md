# OmniThumb high level structure

Could do test first development for all of this.

- [X] Build the "TypeString" system, as follows:
    - TypeString is a superset of mimetype
    - TypeStrings are encoded as follows:

        type string   = format | format ":" argument list;
        format        = mimetype | extension | qualifier;
        mimetype      = [a-z]+"/"[a-z]+;
        extension     = [A-Z]+;                           // e.g. STL, PNG, JPEG
        qualifier     = [a-z]+;                           // e.g. thumb
        argument list = value | value "," argument list;
        value         = [a-z0-9]+;

- [X] Build TypeString tools
    - Guess TypeString from a given input file
    - Output mimetype if it can be easily determined, otherwise extension

- [X] Create ForeignResource class
    - A ForeignResource is a URL, and can be converted to a Resource by
      guessing a TypeString from it

- [X] Create TypedResource class
    - A TypedResource is a URL and a TypeString
    - TypedResources have a property `cache_path`, which is where to cache this
      file

- [X] Build Converter base class
    - Converters have a list of input type strings formats (excluding
      argument list)
    - Converters have a list of output type string format
    - Converters can have a constant estimated conversion time, with 1 being
      fast and large numbers being slow (defaults to 1)
    - Converters have a `convert(in : TypedResource, out : TypedResource)`
      method which will attempt to convert the given resource into the given
      output TypeString. The `to_type` in this case can include arguments.

- [X] Build ConverterGraph class
    - ConverterGraph takes in a list of converters and builds a graph from it
    - ConverterGraph has a method `find_conversion_path(from : TypeString, to :
      TypeString)` outputs an array in the following format, OR raises a
      `ConverterGraph.NoPathFound` exception:

        [
            (Converter, TypeString, TypeString),
            (Converter, TypeString, TypeString),
            ...
        ]

- [X] Build PlaceHolderResponse class
    - PlaceHolderResponse has a list of type string formats that it can
      generate place-holder reponses of
    - e.g. There should be one for all image types that is just a single pixel
      PNG

# Build out contrib

## Thumb / media proof of concept
- [X] Build out the thumb converter

- [X] Build out the media service
    - The media service route has a TypeString in the URL
    - The media service route responds with the converted file, OR a
      placeholder file for that TypeString

- [X] Build out a default settings so it can be run for the original demo

- [X] Contrib placeholder

- [X] Delete old thumb demo code

- [ ] Polish up and add tests for above


## General case

# QoL improvements

- [ ] TypeStringMatcher
    - Can match based on mimetype categories, or custom properties
    - Usable on Placeholders
    - Not usable on Converters, presently, since it would impair creation of
      ConverterGraph

- [ ] Built-in lists of common formats to be used, along with common
  placeholder pixels

- [ ] Built-in regexp for TypeString

# CLI and packaging
- [ ] Decide on name: e.g. `OmniConverter`, or `omnic` for short. Move to
  /omnic/ repo then

- [ ] Fix setup.py packaging, set up pypi
    - [ ] Add to setup.py only the minimum needed packages
    - [ ] Document which packages needed for which contrib stuff

- [ ] Document The Three Uses:
    - Ready-to-go server - Provide docker container to spin up behind nginx,
      using env variables to configure, only providing a settings.py file if
      necessary
    - CLI and library" - Include in other projects (e.g. Django,
      Celery) as a useful conversion utility
    - Web media conversion framework - In the manner of Django, Flask, etc have
      a cookiecutter example of setting up an new project, and hooking in your
      own Services and Converters

- [ ] Expose `omnic` command as follows:
    - `omnic runserver` -- runs a server
    - `omnic convert file.pdf PNG` -- converts from PDF to PNG
    - `omnic convert file.pdf PNG --out=doc.png` -- same as above, but named
    - `omnic render osm-geo:79,32,12 thumb.png` -- renders given thing to PNG
    - `omnic --settings=settings.py <CMD>` -- uses given settings py file
    - `omnic --set-port=8080 <CMD>` -- change individual settings
    - `omnic scaffold new-project` -- scaffolding
    - `omnic scaffold new-service` -- ditto

- [ ] Redis-only commands:
    - `omnic runworker` -- runs a worker-only process
    - `omnic runserverworker` -- runs a process that is both server AND worker
    - `omnic runmulti --worker=1 --server=1 --serverworker=2` -- runs X
      processes of the given types

- [ ] Test suite for CLI

# Future

## Queueing
- [ ] Use: `aioredis` package
- [ ] Allow swapping out asyncio's gimmick-y queuing for a custom-made
  Redis-based async queue (should be easy)
- [ ] Eventually allow attachment of any arbitrary traditional task-queueing
  backend

## Rendering services
- [ ] StringResource - A type of resource where the contents is a short string,
  already in memory

- [ ] /render/ Service - A service that takes in StringResources and outputs
  other things.
    - Example: `/render/osm-geo:79.1239,32.231345,12/thumb.png:200x300/` --- This
      would render Open Street Map into an image, and then use the PNG -> Thumb
      converter to resize to the right size
    - Example: `/render/text3d:"Hello World!"/webm:200x300/` --- This would
      generate Hello World text as 3D shape (obj file), then use the OBJ ->
      WEBM to make a rotating image


## Bundling service
- [ ] zip, tar.gz, tar.bz2, 7z - all bundle formats
- [ ] /bundle/ Service - A service that takes in an URL to a json manifest
  file, which contains an array of files and conversion destinations to be
  processed.
    - Example: [
        {
            "url": "http://host.com/file.png",
            "path": "media/image/file.png",
            "type": "JPG"
        },
        ...
    ]

## WebSocket RPC service
- [ ] /ws/ Service - Exposes all other services via a websocket RPC-like
  interface. Useful for creating more involved progress-bar UIs etc and
  pre-caching longer-running processes
    - Still would have no trust, simply exposing the public HTTP interface in
      another way, for more involved front-end applications
    - Example:
        - `< "media", {url: "foo.com/bar.pdf", typestring="thumb.png"}`
        - `> "downloaded", {url: "foo.com/bar.pdf"}`
        - `> "converting", {url: "foo.com/bar.pdf", type="PNG"}`
        - `> "converting", {url: "foo.com/bar.pdf", type="thumb.png"}`
        - `> "ready", {url: "foo.com/bar.pdf"}`
        - `< "bundle", {url: "foo.com/bar.json"}`
        - `> "in-progress", {url: "foo.com/bar.json"}`
        - `> "downloaded", {url: "foo.com/bar.json"}`
        - `> "downloaded", {url: "foo.com/bar.json"}`

## JS converter
- [ ] Minifier and JSX / TypeScript compiler
- [ ] Possibly a service dedicated to this, or just use /bundle/ wit ha
  different target type ('js')
- [ ] Eliminate build steps for web... stateless serving for all!

## Packaging build server Converters
- [ ] Would play-well with /bundle/
- [ ] Convert "tar.gz" -> rpm, deb, appimage, flatpak etc
- [ ] Convert "python-project.git" -> rpm, deb, appimage, flatpak etc
- [ ] Convert "electron-project.git" -> rpm, deb, appimage, flatpak etc
- [ ] Maybe even EXE generator o.O
- [ ] Maybe loop in game stuff..?


## Mesh
- Blender integration
- Possibly create a JSC3D node module port / fork that uses `node-canvas`, and
  expose a CLI that can render (via software) STL models and such

