from kubernetes import client, config
from kubernetes.client.exceptions import ApiException
from kubernetes.client.rest import ApiException

config.load_kube_config()

apps_v1 = client.AppsV1Api()


def list_deployments():
    deployments = apps_v1.list_namespaced_deployment(namespace="default")
    return deployments.items


def create_deployment(
    app_name,
    image_name,
    replicas=1,
):

    deployment = client.V1Deployment(
        metadata=client.V1ObjectMeta(name=app_name),
        spec=client.V1DeploymentSpec(
            replicas=replicas,
            selector={"matchLabels": {"app": app_name}},
            template=client.V1PodTemplateSpec(
                metadata=client.V1ObjectMeta(labels={"app": app_name}),
                spec=client.V1PodSpec(
                    containers=[
                        client.V1Container(
                            name=app_name,
                            image=image_name,
                        )
                    ]
                ),
            ),
        ),
    )

    response = apps_v1.create_namespaced_deployment(
        namespace="default",
        body=deployment,
    )

    return response


def get_deployment(app_name):

    deployment = apps_v1.read_namespaced_deployment(
        name=app_name,
        namespace="default",
    )

    return deployment


def delete_deployment(app_name):

    response = apps_v1.delete_namespaced_deployment(
        name=app_name,
        namespace="default",
    )

    return response


def get_deployment_status(app_name):

    try:
        deployment = apps_v1.read_namespaced_deployment(
            name=app_name,
            namespace="default",
        )

        status = deployment.status
        spec = deployment.spec
        metadata = deployment.metadata

        desired = spec.replicas or 0
        ready = status.ready_replicas or 0

        if metadata.deletion_timestamp:
            return "Terminating"

        if ready == desired:
            return "Running"

        if 0 < ready < desired:
            return "Scaling"

        if status.conditions:
            for condition in status.conditions:
                if (
                    condition.type == "Progressing"
                    and condition.status == "False"
                    and condition.reason == "ProgressDeadlineExceeded"
                ):
                    return "Failed"

        # deployment created but pods are not ready
        return "Pending"

    except ApiException as e:
        if e.status == 404:
            return "Not Found"

        raise e


if __name__ == "__main__":
    try:
        status = get_deployment_status("mysite-nginx")
        print(status)
    except ApiException as e:
        print(e.status)
        print(e.reason)
        print(e.body)
