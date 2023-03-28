update version in pyproject.toml
python -m build --wheel
python -m twine upload dist/*