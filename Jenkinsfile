node {
    def registryProjet='registry.gitlab.com/remiliance/registrydockerimage'
    def IMAGE="${registryProjet}:version-${env.BUILD_ID}"
    stage('Clone') {
        git 'https://github.com/remiliance/projet_panier_produit.git'
    }
    stage('Build Python') {
        echo 'debut du build'
        sh 'pip install -r requirements.txt'
        docker.build("$IMAGE", '.')
    }
    stage('Test Python') {
        echo 'Test Python'
        sh 'python app/manage.py test'
    }
    stage('Run') {
	    img.withRun("--name run-$BUILD_ID -p 9099:8080") { c->
		sh 'docker ps'
		sh 'netstat -ntaup'
		sh 'sleep 30s'
		sh 'curl 127.0.0.1:8000'
		sh 'docker ps'
	    }

    }
    stage('Push') {
	    docker.withRegistry('https://registry.gitlab.com','reg2') {
		img.push 'latest'
		img.push()
       }
    }
}