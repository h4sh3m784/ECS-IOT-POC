node{
    def app

    stage('Clone repository'){
    /* Let's make sure we have the repository cloned to our workspace */
        checkout scm
    }
    stage('Build Image'){
        /* This builds the actual image: synonymous to
            docker build on the command line */
            bash '''#!/bin/bash
                 echo "hello world" 
                    '''
    }
    // stage('Test image'){
    //     /* Ideally, we would run a test framework against our image */
    //     app.inside{
    //         sh 'echo "Tests passed"'
    //     }
    // }
}