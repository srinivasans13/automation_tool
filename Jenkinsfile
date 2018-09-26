pipeline{
agent any
stages{
stage("parallel stages"){
  parallel{
  script{
    for(i=0;i<5;i++){
      stage("stage${item}"){
        steps{
         echo "stage${item}"
        }
      }
    }
    }
}
}
}
