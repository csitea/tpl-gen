.PHONY: logit ## @-> checks the terraform version
logit:
	@git log --date=iso --pretty --format="%h %<(16)%ad %<(15)%ae ::: %s"

.PHONY: git-crlf ## @-> remove carriage return from all repo
git-crlf:
	@find . -type f -not -path './.git/*' -exec perl -pe  's/\r\n$/\n/g' -i {} \;
