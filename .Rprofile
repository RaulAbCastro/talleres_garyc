local({
  library_path <- file.path(getwd(), ".local", "R", "library")
  dir.create(library_path, recursive = TRUE, showWarnings = FALSE)
  .libPaths(c(library_path, .libPaths()))
  options(repos = c(CRAN = "https://cloud.r-project.org"))
  python_path <- file.path(getwd(), ".venv", "bin", "python")
  if (file.exists(python_path) && !nzchar(Sys.getenv("RETICULATE_PYTHON"))) {
    Sys.setenv(RETICULATE_PYTHON = python_path)
  }
})
