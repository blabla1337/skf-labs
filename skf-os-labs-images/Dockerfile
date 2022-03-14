FROM ghcr.io/linuxserver/baseimage-ubuntu:bionic as builder

ARG GUAC_VER="0.9.14"
ARG BUILD_DIR=/tmp/guacd-docker-BUILD
ARG PKG_NAME="guacd"
ARG BUILD_DEPENDENCIES="          \
	autoconf                      \
	automake                      \
	gcc-6                         \
	libcairo2-dev                 \
	libfreerdp-dev                \
	libjpeg-turbo8-dev            \
	libossp-uuid-dev              \
	libpng-dev                    \
	libpulse-dev                  \
	libssl-dev                    \
	libtool                       \
	libvorbis-dev                 \
	libwebp-dev                   \
	make"

COPY /buildroot /

RUN \
 echo "**** install build deps ****" && \
 apt-get update && \
 apt-get install -qy --no-install-recommends \
	checkinstall \
	curl \
	$BUILD_DEPENDENCIES && \
 echo "**** prep build ****" && \
 mkdir ${BUILD_DIR} && \
 ln -sf /usr/bin/gcc-6 /usr/bin/gcc && \
 curl -o /tmp/guacd.tar.gz -s \
	-L "https://sourceforge.net/projects/guacamole/files/current/source/guacamole-server-${GUAC_VER}.tar.gz" && \
 tar -xf /tmp/guacd.tar.gz --strip=1 -C ${BUILD_DIR} && \
 echo "**** build guacd ****" && \
 cd ${BUILD_DIR} && \
 ./configure --with-init-dir=/etc/init.d --prefix=/usr && \
 make -j 2 CC=gcc-6 && \
 mkdir ${BUILD_DIR}/doc-pak && \
 /bin/list-dependencies.sh \
	"${BUILD_DIR}src/guacd/.libs/guacd" \
	$(find ${BUILD_DIR} | grep "so$") \
	> ${BUILD_DIR}/doc-pak/DEPENDENCIES && \
 PREFIX=/usr checkinstall \
	-y \
	-D \
	--nodoc \
	--pkgname ${PKG_NAME} \
	--pkgversion ${GUAC_VER} \
	--pakdir /tmp \
	--exclude "/usr/share/man","/usr/include","/etc" && \
 mv /tmp/${PKG_NAME}_${GUAC_VER}-*.deb /tmp/${PKG_NAME}_${GUAC_VER}.deb


FROM ghcr.io/linuxserver/baseimage-gui

# set version label
ARG BUILD_DATE
ARG VERSION
LABEL build_version="Linuxserver.io version:- ${VERSION} Build-date:- ${BUILD_DATE}"
LABEL maintainer="HurricaneHrndz"


ARG TOMCAT_VER="tomcat8"
ARG GUAC_VER="0.9.14"
ARG PKG_NAME="guacd"
ARG GUACD_DEPENDENCIES="          \
	ca-certificates               \
	ghostscript                   \
	libfreerdp-plugins-standard   \
	fonts-liberation              \
	fonts-dejavu                  \
	xfonts-terminus"

ENV TOMCAT_VER=${TOMCAT_VER}

# Copy deb into this stage
COPY --from=builder /tmp/${PKG_NAME}_${GUAC_VER}.deb /tmp/${PKG_NAME}_${GUAC_VER}.deb

RUN \
 echo "**** install guacd ****" && \
 dpkg --path-include=/usr/share/doc/${PKG_NAME}/* \
	-i /tmp/${PKG_NAME}_${GUAC_VER}.deb && \
 apt-get update && \
 apt-get install -qy --no-install-recommends \
	${GUACD_DEPENDENCIES} && \
 apt-get install -qy --no-install-recommends \
	$(cat /usr/share/doc/${PKG_NAME}/DEPENDENCIES) && \
 echo "**** install guacamole ****" && \
 mkdir -p \
	/etc/guacamole/extensions \
	/etc/guacamole/lib && \
 apt-get install -qy --no-install-recommends \
	${TOMCAT_VER} \
	${TOMCAT_VER}-common \
	${TOMCAT_VER}-user && \
 curl -so /etc/guacamole/guacamole.war \
	-L https://sourceforge.net/projects/guacamole/files/current/binary/guacamole-${GUAC_VER}.war && \
 echo "GUACAMOLE_HOME=/etc/guacamole" >> /etc/default/${TOMCAT_VER} && \
 ln -s /etc/guacamole /usr/share/${TOMCAT_VER}/.guacamole && \
 curl -so /tmp/guacamole-noauth.tar.gz \
	-L http://archive.apache.org/dist/guacamole/${GUAC_VER}/binary/guacamole-auth-noauth-${GUAC_VER}.tar.gz && \
 mkdir -p /tmp/noauth && \
 tar -xf /tmp/guacamole-noauth.tar.gz --strip=1 -C /tmp/noauth && \
 mv /tmp/noauth/guacamole-auth-noauth-${GUAC_VER}.jar /defaults/ && \
 echo "**** clean up ****" && \
 rm -rf \
	/var/lib/${TOMCAT_VER}/webapps/ROOT \
	/tmp/* \
	/var/lib/apt/lists/* \
	/var/tmp/*

# add local files
COPY /root /

# ports and volumes
EXPOSE 8080
VOLUME /config
