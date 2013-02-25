require 'sinatra'
require 'sequel'

DB = Sequel.connect('mysql://username:password@localhost/sinatra_notes')
notes = DB[:notes]

get '/' do
  ahref = notes.collect {|note| {:name => note[:name],:path => "/note/"+note[:name]+"/"} }
  erb :index, :locals => {:notes => ahref}
end

get '/note/new/' do
  erb :_form, :locals => {:note => {:name => "", :text => ""}}
end

post '/note/new/' do
  notes.insert(params)
  redirect to('/')
end

get '/note/:name/' do |name|
    note = notes.filter(:name => name).first
    erb :show, :locals => {:note => note}
end

post '/note/:namer/' do |name|
    notes.filter(:name => name).update({:name => params[:name], :text => params[:text]})
    redirect to('/')
end

get '/note/:name/delete/' do |name|
  notes.filter(:name => name).delete
  redirect to('/')
end
