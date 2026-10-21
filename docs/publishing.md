# Publish Well-Argued Prose on GitHub

The release examples have been replaced with original editorial reconstructions of published *Mind* arguments, and the project is credited to **Ferdinand Ries**. Confirm that this public identity is the intended attribution before publishing.

1. **Validate the package.** In the extracted `well-argued-prose` folder, run:

   ```bash
   python -m pip install -e .
   python -m well_argued_prose validate
   python -m unittest discover -s tests -v
   python scripts/build_handbook.py --check
   ```

2. **Create the repository.** At GitHub, create a new empty public repository named `well-argued-prose` under `FerdinandRies` (do not initialize a separate README or license). Then run:

   ```bash
   git init
   git add .
   git commit -m "Release Well-Argued Prose v0.1.1"
   git branch -M main
   git remote add origin https://github.com/FerdinandRies/Well-Argued-Prose.git
   git push -u origin main
   ```

3. **Set the project profile.** Suggested short description: “Argument-first standards for top-tier scholarly writing.” Suggested tags: `academic-writing`, `philosophy`, `argumentation`, `scholarly-writing`, `open-source`. Cite this release in GitHub's citation interface after publication.

The repository supplies tests, GitHub Actions, issue templates, a citation file, contribution instructions, and MIT (software) plus CC BY 4.0 (original rulebook and examples) licensing. Its examples paraphrase linked papers; the full original articles are not bundled. The package does not publish itself.
