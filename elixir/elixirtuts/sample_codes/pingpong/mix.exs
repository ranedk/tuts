defmodule PingPong.Mixfile do
  use Mix.Project

  def project do
    [
      version: "0.0.1",
      app: :pingping,
      escript: escript()
    ]
  end

  defp escript do
    [main_module: PingPong.CLI]
  end
end
