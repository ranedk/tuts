defmodule Issues.MixProject do
  use Mix.Project

  def project do
    [
      app: :issues,
      escript: escript_config(),
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
      { :httpoison, "~> 1.0.0" },
      { :poison, "~> 3.1" },
      { :ex_doc, "~> 0.19"},
      { :earmark, "~> 1.3.2"}
      # {:dep_from_hexpm, "~> 0.3.0"},
      # {:dep_from_git, git: "https://github.com/elixir-lang/my_dep.git", tag: "0.1.0"}
    ]
  end

  defp escript_config do
    [
      main_module: Issues.CLI
    ]
  end

end
