from kubernetes import client, config

config.load_kube_config()

apps_v1 = client.AppsV1Api()


def list_deployments():

    deployments = apps_v1.list_namespaced_deployment(
        namespace="default"
    )

    return deployments.items


def create_deployment(
    app_name,
    image_name,
    replicas=1,
):

    deployment = client.V1Deployment(
        metadata=client.V1ObjectMeta(
            name=app_name
        ),
        spec=client.V1DeploymentSpec(
            replicas=replicas,
            selector={
                "matchLabels": {
                    "app": app_name
                }
            },
            template=client.V1PodTemplateSpec(
                metadata=client.V1ObjectMeta(
                    labels={
                        "app": app_name
                    }
                ),
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