from recon_figure4.figure4 import render


def test_renderer_writes_a_nonempty_figure(tmp_path):
    output = render(tmp_path / "figure4.png")
    assert output.exists()
    assert output.stat().st_size > 10_000
