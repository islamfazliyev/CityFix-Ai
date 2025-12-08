# app.rb
require 'sinatra'
require 'sinatra/reloader' if development?
require 'sinatra/activerecord'


# Route to handle the root path

get '/' do
  erb :index
end


get '/forum_detail' do
  erb :forum_detail
end

get '/create_forum' do
  erb :create_forum
end

get '/forums' do
  erb :forums
end

get '/login' do
  erb :login_register
end