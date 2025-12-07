# app.rb
require 'sinatra'
require 'sinatra/reloader' if development?
require 'sinatra/activerecord'

# configure SQlite database
set :database, { adapter: "sqlite3", database: "db/app.db" }

# For installing models (if we say we have models)
require_relative 'models/task'

# Route to handle the root path

get '/' do
  "hello world!"
end

