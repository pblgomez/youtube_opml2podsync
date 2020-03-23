#!/usr/bin/env python

import opml
import re # for replacein characters
import argparse


def create_out_file(outputfile,server,port,youtube,vimeo):

  with open(outputfile,'w') as f_out:
    f_out_content = f'''[server]
hostname = "{server}"
port = {port}
data_dir = "/app/data"

[tokens]
youtube = "{youtube}"
vimeo = "{vimeo}"

[feeds]'''

    f_out.write(f_out_content)


def fill_out_file(inputfile,outputfile):
  nested = opml.parse(inputfile)
  my_dict={}
  length = len(nested[0])

  i=0
  while i < length:
    title=nested[0][i].text
    # Remove special characters
    title = re.sub(r'[^A-Za-z0-9]+', '', title)

    url=nested[0][i].xmlUrl
    ## change feed for channel url
    url = url.replace('feeds/videos.xml?channel_id=','channel/')

    my_dict[title] = url
    i+=1


  with open(outputfile,'a') as f_out:

    for title in sorted(my_dict.keys(), key=lambda line: line.lower().split()):
      # print (title, my_dict[title])
      f_out_content = f'''

      [feeds.{title}]
      url = "{my_dict[title]}"
      page_size = 3 # The number of episodes to query each update (keep in mind, that this might drain API token)
      update_period = "12h" # How often query for updates, examples: "60m", "4h", "2h45m"
      quality = "high" # or "low"
      format = "video" # or "audio"'''
      f_out.write(f_out_content)





### Arguments
parser = argparse.ArgumentParser(description='Converts youtube subscriptions opml to use with podsync')
parser.add_argument('-i', '--input', required=False, help='input filename and/or full path',
                    type=str, dest='inputfile')
parser.add_argument('-o', '--output', help='output filename and/or full path, default ./outfile.toml',
                    type=str, dest='outputfile')
parser.add_argument('-s', '--server', help='server address of podsync',
                    type=str, dest='server')
parser.add_argument('-p', '--port', help='server port of podsync',
                    type=str, dest='port')
parser.add_argument('-y', '--youtube-token',
                    help='youtube token (https://elfsight.com/blog/2016/12/how-to-get-youtube-api-key-tutorial/)',
                    type=str, dest='youtube')
parser.add_argument('-v', '--vimeo-token',
                    help='vimeo token (https://developer.vimeo.com/api/guides/start#generate-access-token)',
                    type=str, dest='vimeo')
args = parser.parse_args()

if args.inputfile:
  inputfile=args.inputfile
else:
  inputfile='subscription_manager'

if not args.outputfile:
  outputfile = 'config.toml'
else:
  outputfile = args.outputfile

if not args.server:
  server='http://192.168.1.100:8089'
else:
  server=args.server

if args.port:
  port=args.port
else:
  port=8089

if args.youtube:
  youtube=args.youtube
else:
  youtube=None

if args.vimeo:
  vimeo=args.vimeo
else:
  vimeo=None
##################################


create_out_file(outputfile,server,port,youtube,vimeo)
fill_out_file(inputfile,outputfile)