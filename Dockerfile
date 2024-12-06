FROM eclipse-temurin:20-jdk

# add --insecure for a quick fix if your network requires certificates
# -L means follow redirects
RUN curl -L -O https://github.com/synthetichealth/synthea/releases/download/master-branch-latest/synthea-with-dependencies.jar
