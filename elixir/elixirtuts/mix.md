# mix - the project manager

Mix is pre-installed with Elixir and is responsible for multiple tasks like dependency management, running scripts, generating docs, building the code etc.

```bash
# To get help from mix
$ mix help

# To start a new project (names issues)
$ mix new issues

# This will create the following structure
issues
├── .formatter.exs
├── .gitignore
├── README.md
├── config
│
└── config.exs
├── lib
│
└── issues.ex
├── mix.exs
└── test
├── issues_test.exs
└── test_helper.exs

# To list all dependencies
$ mix help deps
```

Tests are written inside `test` folder.
```bash
# To run tests
$ mix test
```

Refer to the sample project to understand tests and code flow. Mix is configured using `mix.exs` which is explained below:

```elixir
defmodule Issues.MixProject do
  use Mix.Project

  def project do
    [
      app: :issues,     # name of app
      escript: escript_config(),    # entry script config
      version: "0.1.0",
      elixir: "~> 1.8",
      start_permanent: Mix.env() == :prod,
      deps: deps()
    ]
  end

  # Run "mix help compile.app" to learn about applications.
  def application do
    [
      extra_applications: [:logger]
    ]
  end

  # Run "mix help deps" to learn about dependencies.
  # Beam VM will go through all the dependencies, add them to your
  # application list (defined above in def application) automatically
  # if they are OTP apps with callbacks and need to be started on startup
  # Defining extra_applications, is a way to start internal deps like logger on startup
  # since they cannot be put into deps (already internal to elixir)
  defp deps do
    [
      { :httpoison, "~> 1.0.0" },       # This for e.g. runs as a separate process outside main
      { :poison, "~> 3.1" },
      { :ex_doc, "~> 0.19"},
      { :earmark, "~> 1.3.2"}
      # {:dep_from_hexpm, "~> 0.3.0"},
      # {:dep_from_git, git: "https://github.com/elixir-lang/my_dep.git", tag: "0.1.0"}
    ]
  end

  defp escript_config do
    [
      main_module: Issues.CLI   # For a command line script, this gives the linke to the entry point (main)
    ]
  end

end
```

Based on the above config file:
```shell
# To list deps
$ mix deps

# To download deps
$ mix deps.get

# Package our program using mix:
$ mix escript.build
# generates a binary called 'issues'

# For deployment, you will need to install elixir and erlang with Beam VM
# to run this binary

# To generate docs
# mix docs

```

The file config/config.exs will store all application level constants

To run a particular function in elixir with parameters, you can use

```elixir
$ mix run -e 'Issues.CLI.run(["-h"])'
```

You can find built-in libraries on
- http://elixir-lang.org/docs.html
- http://erlang.org/doc/

External libraries on:
- https://hex.pm

# Tests

## Docs married to tests

The problem with comments is that they just don’t get maintained. The code changes, the comment gets stale, and it becomes useless. Fortunately, ExUnit has doctest , a tool that extracts the iex sessions from your code’s @doc strings, runs it, and checks that the output agrees with the comment.

To invoke it, simply add one or more `doctest ModuleName`
```elixir
defmodule DocTest do
    use ExUnit.Case
    doctest Issues.TableFormatter
end
```
How do we write tests in comments:
```elixir
@doc """
Return a binary (string) version of our parameter.

    ## Examples

    iex> Issues.TableFormatter.printable("a")
    "a"

    iex> Issues.TableFormatter.printable(99)
    "99.0"
"""
```

## Best way to write tests in Elixir
```elixir
defmodule TestStats1 do
    use ExUnit.Case

    describe "Stats on lists of ints" do        # Describe a set of tests by behaviour
        setup do                                # Data fixtures for the test
        [
            list:   [1, 3, 5, 7, 9, 11]
            sum:    36,
            count:  6
        ]
    end

    test "calculates sum", fixture do
        assert Stats.sum(fixture.list) == fixture.sum
    end

    test "calculates count", fixture do
        assert Stats.count(fixture.list) == fixture.countend
    end

    test "calculates average", fixture do
        assert Stats.average(fixture.list) == fixture.sum / fixture.count
    end

end
```

## Property tests - Fake data
You don't always really need to define behavioural tests with sample data
Another option is to generate test data and test generic conditions
e.g. reverse of a string will have the same length
e.g. sum of a list with one element is the element itself

First we need to add a data generator the deps
```elixir
{ :stream_data, ">= 0.0.0" },
```
Writing the test
```elixir
defmodule StatsPropertyTest do
    use ExUnit.Case
    use ExUnitProperties

    describe "Stats on lists of ints" do
        property "single element lists are their own sum" do
            check all number <- integer() do        # integer() generates random integer
                assert Stats.sum([number]) == number
            end
        end
    end
end
```

```bash
$ mix coveralls         // Get Test coverage stats
$ mix coveralls.html    // Generate HTML report. Also integrates with CI systems
```

# Debugging
Like the ipython shell, you can start the `iex` repl inside the code using:
```elixir
require IEx; IEx.pry
```

For a mix app, start iex debugger by loading all modules
```shell
$ iex -S mix
```

# Utilities
Mix provides a lot of utilities code analysis:

```shell
$ mix xref unreachable      // List functions that are not known at the time they are called
$ mix xref warnings         // Get warnings for unknown functions

$ mix xref graph --format dot   // Create dependency tree
$ dot -Grankdir=LR -Epenwidth=2 -Ecolor=#a0a0a0 -Tpng xref_graph.dot -o xref_graph.png // Create png of dependency tree

$ mix xref callers Mod | Mod.func | Mod.func/arity  // To get callers of a module or a function
```

# Monitoring
Inside iex
`iex> :observer.start()` will start a memory, CPU monitoring tool
This requires external packages etc. mostly provided by frameworks.

Third party apps are available for do application level monitoring e.g. Elixometer by Pintrest
