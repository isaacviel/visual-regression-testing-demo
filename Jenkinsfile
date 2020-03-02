#!/usr/bin/env groovy

def agentLabel = 'afdAgent'
def imageName = 'vrt'
def vrtImage = ''
def imageOptions = '-e 8043  --hostname vrtDemo --network traefik --name vrtDemo'
def traefikOptions = '-l traefik.enable="true" -l traefik.http.routers.vrt.entrypoints="web" -l traefik.http.services.vrt.server.port="8043" -l traefik.http.routers.vrt.rule="Host(`agent.local`)"'

pipeline {

  agent { label agentLabel}

  stages {

    stage('build') {
        steps {
          echo "going to docker build phase"
          script {
              vrtImage = docker.build("${imageName}:${env.BUILD_ID}")
          }
        }
    }

    stage('run') {
      steps {
          echo "going to run docker image phase"
          script {
              vrtImage.run("${imageOptions} ${traefikOptions}")
            }

      }

    }
	}
}
