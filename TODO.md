# Next steps:

## Top priority
- [ ] Build out full unit tests for new features
    - [X] Worker
    - [ ] Server
    - [ ] Convert utilities

- [ ] Build out full integration tests for contrib
    - [ ] Mock out all spawn calls
    - [ ] CLI interface

- [ ] QoL settings improvement
    - [ ] Make settings like Django so you import where you need
      instead of pass around a "config" object
    - [ ] Add import system like Django's, so that `settings.py` doesn't need
      to import anything

## Done
- [X] Finish doc -> thumb proof of concept
    - [X] ExecConverter needs a "rename from" feature, that allows you to
      specify an output file that differs in name from the one that is expected

- [X] Need a few more file types to provide proper proof of concept
    - [X] DOC -> PDF
    - [X] PDF first page -> PNG (depends on above)
    - [X] OBJ/MESH/etc -> STL (meshlab)
    - [X] STL,OBJ -> PNG (jsc3d)
    - [X] Molecule file conversion and visualization, just because

## Misc

- [ ] Work on some very simple refresh javascript to integrate

- [ ] Fix running unoconv within venv
    - [ ] Check if in virtualenv and ensure environments Python is used when
      doing subprocess calls

- [ ] Rename contrib to `builtins` (?)

- [ ] QoL conversion grid improvements:
    - [ ] Think more about how to make extension "supersede" mimetype in a
      reliable way
    - [ ] Add "configure" check to base Converter, which should ensure correct
      Python and system packages installed for the converter to be functoinal
    - [ ] Allow conversions to self
    - [ ] Allow preferred conversion paths in settings, which are picked first
      if available, e.g. like the following:
        {
            ('STL', 'JPG'): ['STL', 'PNG', 'add_background.png', 'JPG:1000x1000'],
        }

- [ ] AsyncIO improvements
    - [ ] Replace all file system calls with aiofiles
    - [ ] Replace all spawn system calls with asyncio equivalent


# Look into 3D rendering

- [X] Work on JSC3D CLI
    - [X] Integrate JSC3D with node canvas
    - [X] STL -> PNG

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

# CLI and packaging
- [ ] Decide on name: e.g. `OmniConverter`, or `omnic` for short. Move to
  /omnic/ repo then

- [ ] Fix setup.py packaging, set up pypi
    - [ ] Add to setup.py only the minimum needed packages
    - [ ] Document which packages needed for which contrib stuff

- [ ] Document the three uses:
    - CLI and library - Include in other projects (e.g. Django, Celery) as a
      useful conversion utility
    - Ready-to-go server - Provide docker container to spin up behind nginx,
      using env variables to configure, only providing a settings.py file if
      necessary
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


# Admin and demo

### Admin service
- [ ] Admin panel should use /ws/ backend to provide a graphical view of the
  process of files being ingested

- [ ] Very simple panel:
    1. Paste in a URL
    2. It downloads and converts to TypedForeignResource
    3. It shows all possible paths from that filetype
    4. Clicking on one will swap it with an embedded viewer (if
    applicable)

# Future

## JS viewer system

- First API call looks for all `img[omnic-viewer]` and
  `img[omnic-embed]` tags and sends 1 AJAX call to check if they are all
  loaded.
    - If not, it will add a spinner to all thumbnails of them, and try
      again in X seconds (V2: could keep running average of every
      conversion path, and try again in `avg * 1.5` or something)
    - If loaded, it will check if omnic-viewer, then add a hoverable (>)
      button in the center, and an onclick event which will activate the
      appropriate viewer
    - If possible / cheap computationally, avoid API calls by checking
      if the image is a 1x1 placeholder image (?)
- [ ] New Viewer system: Each type can have a Viewer, that serves up JS
  that mounts a viewer on a particular element (given a URL). E.g. the
  STL, OBJ etc viewer, when clicked on, will enable JSC3D.
    - [ ] All registered viewers get served up on page load in one
      minified JS bundle
    - [ ] They only get "activated" as needed
- [ ] Embed in page components
    - `<img src="...omnic/media/thumb.jpg..." omnic-viewer="PDF" />`
    - The JS looks for all tags with `[omnic-viewer]` and adds a click
      event that will embed the correct type of viewer for that element

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
- [X] Possibly create a JSC3D node module port / fork that uses `node-canvas`,
  and expose a CLI that can render (via software) STL models and such
- [ ] DXF

# QoL improvements

- [ ] TypeStringMatcher
    - Can match based on mimetype categories, or custom properties
    - Usable on Placeholders
    - Not usable on Converters, presently, since it would impair creation of
      ConverterGraph

- [ ] Built-in lists of common formats to be used, along with common
  placeholder pixels

- [ ] Built-in regexp for TypeString

# Performance and stability improvements

- [ ] Performance hack: Have a "sticky queue" system where resources go into
  several worker queues based on hash on URI
    - More importantly this would allow processing multiple resources at once,
      and assumedly max out CPU better e.g. if waiting on slow net IO, could be
      using that CPU for local conversion
    - [ ] Long term solution: Allow task ordering in work queue system
        - This would allow download + all conversions be queued w.r.t. each other

