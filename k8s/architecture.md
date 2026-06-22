# Hitcounter System Diagram

```mermaid
flowchart LR
  User[User Browser]
  DNS[notoriousmeowmeow.com\nA → LoadBalancer IP]

  subgraph GKE["GKE Cluster"]
    LB[LoadBalancer Service\nhitcounter-service]
    App1[hitcounter Pod 1\nimage: mshummingbirb/my-hit-counter:v3]
    App2[hitcounter Pod 2\nimage: mshummingbirb/my-hit-counter:v3]
    RedisSvc[Service\nredis-service]
    RedisPod[redis Pod\nimage: redis:7]
  end

  User -->|HTTP 80| DNS --> LB
  LB --> App1
  LB --> App2
  App1 -->|TCP 6379| RedisSvc
  App2 -->|TCP 6379| RedisSvc
  RedisSvc --> RedisPod
  App1 -->|HTTP /healthz| App1
  App2 -->|HTTP /healthz| App2