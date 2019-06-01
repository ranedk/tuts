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

# Dependency graphs

- The base of all application is a supervisor app, which will manage crashes of all apps.
- This base supervisor will manage:
    - Independent apps
    - Apps depended on independent apps
    - Supervisor app, which manages multiple-process apps
