FROM ruby:2.3.7

COPY / /files/
RUN apt-get update && apt-get install -y \ 
  build-essential \ 
  nodejs
RUN mkdir -p /app 
WORKDIR /app

# Copy the Gemfile as well as the Gemfile.lock and install 
# the RubyGems. This is a separate step so the dependencies 
# will be cached unless changes to one of those two files 
# are made.
COPY Gemfile Gemfile.lock ./ 
RUN gem update --system
RUN gem install bundler && bundle install --jobs 20 --retry 5

# Copy the main application.
COPY . ./
RUN rake db:drop db:create db:migrate db:seed
# Expose port 3000 to the Docker host, so we can access it 
# from the outside.
EXPOSE 3000

# The main command to run when the container starts. Also 
# tell the Rails dev server to bind to all interfaces by 
# default.
CMD ["bundle", "exec", "rails", "server", "-b", "0.0.0.0"]


