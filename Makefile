deploy:
	bundle exec jekyll build -c _config.yml,_config-prod.yml
	git add .
	git commit -am 'deploy'
	git push

dev:
	bundle exec jekyll serve
