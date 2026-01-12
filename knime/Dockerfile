# KNIME Analytics Platform Docker Image
# Note: This is a minimal setup. For production, consider using official KNIME Server

FROM ubuntu:22.04

# Install dependencies
RUN apt-get update && apt-get install -y \
    wget \
    openjdk-17-jdk \
    libgtk-3-0 \
    libwebkit2gtk-4.0-37 \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /opt

# Download KNIME Analytics Platform
# Note: You need to download the Linux version from https://www.knime.com/downloads
# and place it in the knime/ directory before building
# Example: knime_5.2.0.linux.gtk.x86_64.tar.gz

# For now, create a placeholder
RUN echo "KNIME Analytics Platform" > /opt/README.txt && \
    echo "To use KNIME in Docker:" >> /opt/README.txt && \
    echo "1. Download KNIME Linux version from https://www.knime.com/downloads" >> /opt/README.txt && \
    echo "2. Extract to /opt/knime" >> /opt/README.txt && \
    echo "3. Rebuild this image" >> /opt/README.txt

# Expose KNIME Server port (if using KNIME Server)
EXPOSE 8080

# Command to run KNIME
CMD ["cat", "/opt/README.txt"]
