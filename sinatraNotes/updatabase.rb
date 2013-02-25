require 'sequel'
require 'rubygems'


DB = Sequel.connect('mysql://root:8Characters!@localhost/sinatra_notes')

DB.create_table :notes do
  varchar :name, :primary_key => true
  String :text
end

notes = DB[:notes]

notes.insert(:name => "test", :text => "hello everyone!")\


puts notes.first