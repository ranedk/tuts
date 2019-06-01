# Designing applications

Questions to ask before designing elixir application

- What are the different modules in the app
    - Modules in Elixir are processes
    - Each module will be a process and will have a supervisor
    - Some module may be a collection of multiple processes
        - May have one supervisor each process
        - May have one supervisor for all process
- What is a API for each module
    - APIs send an action and the data to act upon
    - Each api call should finish before 5 seconds(Genserver timeout)
    - Hence, instead of looping, they should listen and work
- How is their dependency graph
    - If a process sends data, it depends on the receiver process to work to listen and be up.
- Crash policy for all modules and their processes

Checkout the duper app in sample_codes folder.

Run the super application using `$ mix run --no-halt`

# Dependency graphs

- The base of all application is a supervisor app, which will manage crashes of all apps.
- This base supervisor will manage:
    - Independent apps
    - Apps depended on independent apps
    - Supervisor app, which manages multiple-process apps

# OTP Applications
OTP applications are actually Components or libraries.
When you use an external application, it may start its own processes and supervisors

In the `mix.exs` file, the `def application` tells the main application to pickup.
In the `application.ex` file, you define the `start` function which starts the app and its supervisors

Best practice is to put variables in `environment` and read from `application.ex`
in mix.exs
```elixir
def application
  [
    mod: {Sequence, []}
    env: [initial_number: 46]
    registered: [Sequence.Server]
  ]
end
```
in `application.ex`
```elixir
defmodule Sequence do
    use Application

    def start(_type, _args) do
        Sequence.Supervisor.start_link(Application.get_env(:sequence, :initial_number))
    end
end
```

# Distillery
Used for deployment management.
It can create a single binary with all dependiences.
Also, you can create a migration from one version to another, which will update the code and apply the in-memory data migrations.
