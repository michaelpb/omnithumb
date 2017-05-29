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
- [ ] Build out the thumb converter

- [ ] Build out the media service
    - The media service route has a TypeString in the URL
    - The media service route responds with the converted file, OR a
      placeholder file for that TypeString

- [ ] Build out a default settings so it can be run for the original demo

- [ ] Clean up old thumb demo

# QoL improvements

- [ ] TypeStringMatcher
    - Can match based on mimetype categories, or custom properties
    - Usable on Placeholders
    - Not usable on Converters, presently, since it would impair creation of
      ConverterGraph

- [ ] Built-in lists of common formats to be used, along with common
  placeholder pixels

- [ ] Built-in regexp for TypeString

# Misc other programs

- Possibly create a JSC3D node module port / fork that uses `node-canvas`, and
  expose a CLI that can render (via software) STL models and such

