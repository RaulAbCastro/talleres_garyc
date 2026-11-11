options(repos = c(CRAN = "https://cloud.r-project.org"), timeout = 600)
packages <- c("languageserver", "systemfonts", "httpgd", "reticulate")
# Actualizar los paquetes de Ubuntu anteriores a las API que usamos.
minimum_versions <- c(systemfonts = "1.3.2", reticulate = "1.40.0")
available <- function(package) {
  path <- find.package(package, lib.loc = .libPaths(), quiet = TRUE)
  if (!length(path)) return(FALSE)
  !(package %in% names(minimum_versions)) ||
    packageVersion(package, lib.loc = dirname(path)) >= minimum_versions[[package]]
}
missing <- packages[!vapply(packages, available, logical(1))]
if (length(missing)) {
  install.packages(missing, Ncpus = min(2L, parallel::detectCores()))
}
unavailable <- packages[!vapply(packages, available, logical(1))]
if (length(unavailable)) {
  stop("No se pudieron instalar: ", paste(unavailable, collapse = ", "))
}

# Las versiones nuevas de vscode-R incluyen su propio puente de sesiones.
# Usar la copia de la extensión instalada para mantener su protocolo compatible.
session_sources <- Sys.glob(path.expand(c(
  "~/.vscode-remote/extensions/reditorsupport.r-*/dist/resources/sess",
  "~/.vscode-server/extensions/reditorsupport.r-*/dist/resources/sess"
)))
if (length(session_sources)) {
  versions <- vapply(session_sources, function(path) {
    read.dcf(file.path(path, "DESCRIPTION"), fields = "Version")[[1L]]
  }, character(1))
  session_source <- session_sources[order(package_version(versions), decreasing = TRUE)[1L]]
  field <- "Config/vscode-R/source-revision"
  expected <- read.dcf(file.path(session_source, "DESCRIPTION"), fields = field)[[1L]]
  installed <- find.package("sess", lib.loc = .libPaths(), quiet = TRUE)
  actual <- if (length(installed)) {
    read.dcf(file.path(installed, "DESCRIPTION"), fields = field)[[1L]]
  } else ""
  if (!identical(expected, actual)) {
    install.packages(session_source, repos = NULL, type = "source")
  }
  stopifnot(requireNamespace("sess", quietly = TRUE))
}
