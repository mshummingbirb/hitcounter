# Hitcounter Deployment Diagram

This diagram shows where Docker fits in the workflow.

```mermaid
flowchart TB
  subgraph Local["Local Development"]
    Dev[Developer laptop]
    DockerBuild[Docker build]
    DockerHub[Docker Hub\nmshummingbirb/my-hit-counter:v3]
  end

  subgraph GCP["Google Cloud / GKE"]
    GKECluster[GKE Cluster]
    LB[LoadBalancer Service\nhitcounter-service]
    HitPod1[hitcounter Pod 1\nimage: mshummingbirb/my-hit-counter:v3]
    HitPod2[hitcounter Pod 2\nimage: mshummingbirb/my-hit-counter:v3]
    RedisSvc[Service\nredis-service]
    RedisPod[redis Pod\nimage: redis:7]
    ContainerRuntime[Node runtime\ncontainerd]
  end

  User[User Browser]
  DNS[notoriousmeowmeow.com\nA → LoadBalancer IP]

  Dev --> DockerBuild
  DockerBuild --> DockerHub
  DockerHub -->|pull image| ContainerRuntime
  ContainerRuntime --> HitPod1
  ContainerRuntime --> HitPod2

  User --> DNS --> LB
  LB --> HitPod1
  LB --> HitPod2
  HitPod1 --> RedisSvc
  HitPod2 --> RedisSvc
  RedisSvc --> RedisPod