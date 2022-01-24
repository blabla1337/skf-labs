FROM ruby:2.3.7

# Installing dependencies
RUN apt-get update && apt-get install -y \ 
  build-essential \ 
  nodejs

# Exposing port 3000 for connecting to the application -p 3000:3000
EXPOSE 5000

# Cloning SKF's parameter-binding's application
RUN git clone https://github.com/blabla1337/skf-labs.git

# Changing directory to the application -- for processing stuff later on
WORKDIR /skf-labs/parameter-binding

# Updating/Installing
RUN gem update --system

# Installing bundler and installing gems required for the rails application to run
RUN gem install bundler && \
	bundle install --jobs 20 --retry 5

# Executing Rake's database commands
RUN rake db:drop db:create db:migrate db:seed

# Newly added instructions for getting /bin/ directory from a new application created
# to run our own application -- due to some reason the application released/added on
# the skf-labs doesn't have /bin/ directory in it -- which is required for the application
# to work.

# The following will create a new application with minimal config (required) and will then
# move the /bin/ directory in our parameter-binding challenge directory and delete that
# application later on. Solves the issue!
RUN rails new testApplicationForBinDirectoryOnly --skip-namespace --skip-yarn --skip-gemfile --skip-git --skip-keeps --skip-action-mailer --skip-active-record --skip-active-storage --skip-puma --skip-action-cable --skip-sprockets --skip-spring --skip-listen --skip-coffee --skip-javascript --skip-turbolinks --skip-test --skip-system-test --skip-bootsnap --skip-bundle --no-rc && \
	mv testApplicationForBinDirectoryOnly/bin/ . && \
	rm -rfv testApplicationForBinDirectoryOnly/

# Running rails server with 0.0.0.0 as host in docker and default port (i.e. 3000)
CMD ["bundle", "exec", "rails", "server", "-p", "5000", "-b", "0.0.0.0"]