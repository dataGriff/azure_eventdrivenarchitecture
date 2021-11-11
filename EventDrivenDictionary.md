Event Driven Architecture Dictionary

* **Event** - Immutable business fact stated in the past tense. This could be something new being created or the change in state of something that already exists e.g. *Customer Created* or *Customer Email Updated*. It is important that the event is declared in the past tense during design as consumers of these events expect the event to be a source of immutable truth of something that has definitely happened.
* **Implementation Detail** - Anything prior to the production of a business event is an implementation detail. The technology and complexity, no matter how difficult, are secondary to the target event schema that needs to be produced. This means that there is loong-term decoupling from any subscriber to the event and therefore any technology, in particular storage and local schemas, being used by the producer. 
* **Common Interface** - An Event driven architecture aims to provide a common interface for all applications and data pipelines to publish and subscribe to. This is provided by an event broker. This common interface solves a lot of local specialized implementations to provide data between business areas. 
* **Data Products** - Much like the way that applications and websites are treated as products, the production of the data as events should also be treated as products and evolve incrementally to customer requirements just like any other product.
* **Product Owner** - Product owners are needed for the events that are produced in an event driven architecture to ensure they continue to meet business needs.
* **Team Ownership** - It is extremely important that individual events are owned within single long-lived teams. The team will take the responsibility of producing and adhering to the business agreed schema as well as communicating to subscribers when there are any breaking changes. The events themselves should be treated as products produced by the team and be a part of the teams product owner remit. 
* Producer
* Consumer
* Event Broker
* Event Broker Log
* **Partition** - Important note that consumer groups to partitions should not have more than a 1:1 mapping. Therefore it is important for standard event hubs for example to start with the right amount of partitions if you expect multiple consumers in the future. With premium event hubs and kafka I believe you can dynamically add partitions and therefore consumers.
* Schema Registry
* Topic 
* **Event Storming** - This is the collaborative design of discovering events within and across business domains. This design process should involve all domain experts, business and technical, to derive a common model of the processes and a common language. Event storming is particularly important to get a business-wide view of the events as it can influence schema design to ensure data communication pathways remain robust even with consumer agnostic approachs to event publication by the producer. 
* **Streaming** - Streaming is the idea that data in an event driven architecture there is constantly "data-in-motion" as opposed to "data-at-rest". Applications and data pipelines are able to receive data from a dedicated consumer group without the need for watermarking as the event broker will guarantee at least once delivery and push data to its destination.
* **Immutable Log** - Log not a queue. 