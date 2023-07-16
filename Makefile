build-build:
	docker build -t php-image-build --target build .

build:
	docker build -t php-image .

start-build:
	docker run --rm -it php-image-build ash
