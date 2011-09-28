
def main(q, i, params, service,job,tags, tasklet):

    print ('executing tasklet %s ' % (tasklet.path))

    params.name
    params.space

    '''
    def testWorker(a, b):
        return a+b
    worker=service.getWorker()  #standard is local worker
    calc = worker.tasksubmit(testWorker, 12, 34)
    params.calc = calc
    print calc

    worker=service.getworker(nodeip="192.15.5.5")  #on worker based on ip
    worker=service.getworker(nodename="myLinux")  #on worker based on nodename
    workers=service.getworkers(servicename="*aservicename*",maxNrWorkersPerNode=1)
    workers=service.getworkers(maxNrWorkersPerNode=1)  #all workers in cluster but max 1 per node
    workers=service.getworkers()  #all workers
    for worker in workers:
        worker.tasksubmit(copyfiles,a,b) #executes function copyfiles with params a,b in parallel python (workers)
    '''

    '''
    cluster=service.cluster
    #we can now call methods from same cluster
    service2=cluster.services.iaasmanager.get()
    service2=cluster.services.iaasmanager.getRemote(nodeName="vbnode1")
    service2=cluster.services.iaasmanager.getRemote(serviceInstanceName="virtualboxServer1") #has optionally a name
    service2=cluster.services.iaasmanager.getMaster()  #1 master per service per cluster
    service.vmachine.start(guid="11111sfsdfsf11")
    '''


    return params


def match(q, i, params, service,job,tags, tasklet):
    return True

