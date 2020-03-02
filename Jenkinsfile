#!/usr/bin/env groovy

def agentLabel = 'afdAgent'
def imageName = 'vrt'
def vrtImage = ''

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
              vrtImage.run("-p 4200:8043")
            }

      }

    }
	}
}
