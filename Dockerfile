FROM php:8.2-fpm-alpine3.18 AS build

RUN apk update
RUN apk add musl-utils python3 gcc g++ autoconf make

RUN printf "\n" | pecl install redis \
	&& docker-php-ext-enable redis

RUN mv "$PHP_INI_DIR/php.ini-production" "$PHP_INI_DIR/php.ini"

COPY get-deps.py /usr/local/bin
RUN chmod a+x /usr/local/bin/get-deps.py
RUN python3 /usr/local/bin/get-deps.py

FROM scratch

COPY --from=build /tmp/dest /
COPY --from=build /usr/local/etc/php /usr/local/etc/php/
COPY --from=build /usr/local/etc/php-fpm.d /usr/local/etc/php-fpm.d/
COPY --from=build /usr/local/etc/php-fpm.conf /usr/local/etc/php-fpm.conf
COPY /docker-fs /
ENV PATH=/usr/local/sbin

ENTRYPOINT [ "php-fpm", "--nodaemonize" ]
