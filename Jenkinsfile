#!/usr/bin/env groovy

def agentLabel = 'afdAgent'
def imageName = 'vrt'

pipeline {

  agent { label agentLabel}

  stages {

    stage('build') {
        steps {
          echo "going to docker build phase"
          script {
            def vrtImage = docker.build("${imageName}:${env.BUILD_ID}")
          }
        }
    }

    stage('run') {
      steps {
          echo "going to run docker image phase"
          script {
              vrtImage.run("-p 4200:4200")
            }


    }
	}
}
