pipeline {
  agent any
  stages {
    stage('build') {
      steps {
        echo 'Starting Build Step'
        sh 'mvn clean install -Dlicense.skip=true'
        echo 'Build step complete'
      }
    }

    stage('Testing stage') {
      parallel {
        stage('Testing stage') {
          steps {
            sh 'mvn sonar:sonar -Dsonar.host.url=http://<IP address>:8081 -Dlicense.skip=true'
          }
        }

        stage('SonarQube Test') {
          steps {
            echo "The tester is ${TESTER}"
            sleep 10
          }
        }

        stage('Print Build Number') {
          steps {
            echo "This is build number ${BUILD_ID}"
            sleep 20
          }
        }

      }
    }

    stage('JFrog Push') {
      steps {
        echo 'Starting JFrog Push'
        script {
          def server = Artifactory.server "artifactory"
          def buildInfo = Artifactory.newBuildInfo()
          def rtMaven = Artifactory.newMavenBuild()
          rtMaven.tool = 'maven'
          rtMaven.deployer server: server, releaseRepo: 'libs-release-local', snapshotRepo: 'libs-snapshot-local'
          buildInfo = rtMaven.run pom: 'pom.xml', goals: "clean install -Dlicense.skip=true"
          buildInfo.env.capture = true
          buildInfo.name = 'jpetstore-6'
          server.publishBuildInfo buildInfo
        }

        echo 'JFrog Push Finished'
      }
    }

    stage('Deploy Prompt') {
      steps {
        input 'Deploy to Production?'
      }
    }

    stage('Deployment') {
      steps {
        echo 'Starting Deployment'
        echo 'Deployment Complete'
      }
    }

  }
  environment {
    TESTER = 'Matthew'
  }
}