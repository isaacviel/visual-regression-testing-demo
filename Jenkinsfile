#!/usr/bin/env groovy

def agentLabel = 'afdAgent'
def imageName = 'vrt'
def vrtImage = ''
def vrtName = 'vrtDemo'
def siteName = 'vrt.afd.geocloud.com'
def imageOptions = "-e 8043  --hostname ${vrtName} --network traefik --name vrtDemo"
def traefikOptions = '-l traefik.enable="true" -l traefik.http.routers.vrt.entrypoints="web" -l traefik.http.services.vrt.loadbalancer.server.port="8043" -l traefik.http.routers.vrt.rule="Host(\\`${vrtDemo}\\`)"'

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

    stage('stop') {

      steps {
        catchError {
          echo "stopping any running ${vrtName}"
          script {
              sh """
                docker ps -a \
                | awk '{ print \$1,\$2 }' \
                | grep ${vrtName} \
                | awk '{print \$1 }' \
                | xargs -I {} docker stop {}
                """
            }
            echo "stopping any running ${vrtName}"
          script {
              sh """
                docker ps -a \
                | awk '{ print \$1,\$2 }' \
                | grep ${vrtName} \
                | awk '{print \$1 }' \
                | xargs -I {} docker rm {} || 
                """
          }
        }
      }
    }

    stage('run') {
      steps {
        echo "going to run docker image phase"
        echo "${traefikOptions}"
        script {
          vrtImage.run("${imageOptions} ${traefikOptions}")
        }
      }
    }
	}
}
