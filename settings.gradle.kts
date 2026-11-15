pluginManagement {
    repositories { google(); mavenCentral(); gradlePluginPortal() }
}
dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {
        google(); mavenCentral()
        // Pleos Connect SDK (ai.pleos.playground:*)
        maven { url = uri("https://nexus-playground.pleos.ai/repository/maven-releases") }
    }
}
rootProject.name = "loop-pleos"
include(":app")
