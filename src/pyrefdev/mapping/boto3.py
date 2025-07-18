VERSION = "1.38.46"

# fmt: off
MAPPING = {
    "boto3": "https://boto3.amazonaws.com/v1/documentation/api/latest/index.html",
    "boto3.client": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/boto3.html#boto3.client",
    "boto3.dynamodb": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/customizations/dynamodb.html",
    "boto3.dynamodb.conditions": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/customizations/dynamodb.html",
    "boto3.dynamodb.conditions.attr": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/customizations/dynamodb.html#boto3.dynamodb.conditions.Attr",
    "boto3.dynamodb.conditions.attr.attribute_type": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/customizations/dynamodb.html#boto3.dynamodb.conditions.Attr.attribute_type",
    "boto3.dynamodb.conditions.attr.begins_with": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/customizations/dynamodb.html#boto3.dynamodb.conditions.Attr.begins_with",
    "boto3.dynamodb.conditions.attr.between": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/customizations/dynamodb.html#boto3.dynamodb.conditions.Attr.between",
    "boto3.dynamodb.conditions.attr.contains": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/customizations/dynamodb.html#boto3.dynamodb.conditions.Attr.contains",
    "boto3.dynamodb.conditions.attr.eq": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/customizations/dynamodb.html#boto3.dynamodb.conditions.Attr.eq",
    "boto3.dynamodb.conditions.attr.exists": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/customizations/dynamodb.html#boto3.dynamodb.conditions.Attr.exists",
    "boto3.dynamodb.conditions.attr.gt": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/customizations/dynamodb.html#boto3.dynamodb.conditions.Attr.gt",
    "boto3.dynamodb.conditions.attr.gte": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/customizations/dynamodb.html#boto3.dynamodb.conditions.Attr.gte",
    "boto3.dynamodb.conditions.attr.is_in": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/customizations/dynamodb.html#boto3.dynamodb.conditions.Attr.is_in",
    "boto3.dynamodb.conditions.attr.lt": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/customizations/dynamodb.html#boto3.dynamodb.conditions.Attr.lt",
    "boto3.dynamodb.conditions.attr.lte": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/customizations/dynamodb.html#boto3.dynamodb.conditions.Attr.lte",
    "boto3.dynamodb.conditions.attr.ne": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/customizations/dynamodb.html#boto3.dynamodb.conditions.Attr.ne",
    "boto3.dynamodb.conditions.attr.not_exists": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/customizations/dynamodb.html#boto3.dynamodb.conditions.Attr.not_exists",
    "boto3.dynamodb.conditions.attr.size": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/customizations/dynamodb.html#boto3.dynamodb.conditions.Attr.size",
    "boto3.dynamodb.conditions.key": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/customizations/dynamodb.html#boto3.dynamodb.conditions.Key",
    "boto3.dynamodb.conditions.key.begins_with": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/customizations/dynamodb.html#boto3.dynamodb.conditions.Key.begins_with",
    "boto3.dynamodb.conditions.key.between": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/customizations/dynamodb.html#boto3.dynamodb.conditions.Key.between",
    "boto3.dynamodb.conditions.key.eq": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/customizations/dynamodb.html#boto3.dynamodb.conditions.Key.eq",
    "boto3.dynamodb.conditions.key.gt": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/customizations/dynamodb.html#boto3.dynamodb.conditions.Key.gt",
    "boto3.dynamodb.conditions.key.gte": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/customizations/dynamodb.html#boto3.dynamodb.conditions.Key.gte",
    "boto3.dynamodb.conditions.key.lt": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/customizations/dynamodb.html#boto3.dynamodb.conditions.Key.lt",
    "boto3.dynamodb.conditions.key.lte": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/customizations/dynamodb.html#boto3.dynamodb.conditions.Key.lte",
    "boto3.dynamodb.types": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/customizations/dynamodb.html",
    "boto3.dynamodb.types.binary": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/customizations/dynamodb.html#boto3.dynamodb.types.Binary",
    "boto3.nullhandler": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/boto3.html#boto3.NullHandler",
    "boto3.nullhandler.emit": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/boto3.html#boto3.NullHandler.emit",
    "boto3.resource": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/boto3.html#boto3.resource",
    "boto3.resources.action": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/resources.html#module-boto3.resources.action",
    "boto3.resources.action.batchaction": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/resources.html#boto3.resources.action.BatchAction",
    "boto3.resources.action.custommodeledaction": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/resources.html#boto3.resources.action.CustomModeledAction",
    "boto3.resources.action.custommodeledaction.inject": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/resources.html#boto3.resources.action.CustomModeledAction.inject",
    "boto3.resources.action.serviceaction": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/resources.html#boto3.resources.action.ServiceAction",
    "boto3.resources.action.waiteraction": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/resources.html#boto3.resources.action.WaiterAction",
    "boto3.resources.base": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/resources.html#module-boto3.resources.base",
    "boto3.resources.base.resourcemeta": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/resources.html#boto3.resources.base.ResourceMeta",
    "boto3.resources.base.resourcemeta.client": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/resources.html#boto3.resources.base.ResourceMeta.client",
    "boto3.resources.base.resourcemeta.copy": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/resources.html#boto3.resources.base.ResourceMeta.copy",
    "boto3.resources.base.resourcemeta.data": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/resources.html#boto3.resources.base.ResourceMeta.data",
    "boto3.resources.base.resourcemeta.identifiers": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/resources.html#boto3.resources.base.ResourceMeta.identifiers",
    "boto3.resources.base.resourcemeta.service_name": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/resources.html#boto3.resources.base.ResourceMeta.service_name",
    "boto3.resources.base.serviceresource": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/resources.html#boto3.resources.base.ServiceResource",
    "boto3.resources.base.serviceresource.meta": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/resources.html#boto3.resources.base.ServiceResource.meta",
    "boto3.resources.collection": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/collections.html",
    "boto3.resources.collection.collectionfactory": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/collections.html#boto3.resources.collection.CollectionFactory",
    "boto3.resources.collection.collectionfactory.load_from_definition": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/collections.html#boto3.resources.collection.CollectionFactory.load_from_definition",
    "boto3.resources.collection.collectionmanager": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/collections.html#boto3.resources.collection.CollectionManager",
    "boto3.resources.collection.collectionmanager.all": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/collections.html#boto3.resources.collection.CollectionManager.all",
    "boto3.resources.collection.collectionmanager.filter": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/collections.html#boto3.resources.collection.CollectionManager.filter",
    "boto3.resources.collection.collectionmanager.iterator": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/collections.html#boto3.resources.collection.CollectionManager.iterator",
    "boto3.resources.collection.collectionmanager.limit": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/collections.html#boto3.resources.collection.CollectionManager.limit",
    "boto3.resources.collection.collectionmanager.page_size": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/collections.html#boto3.resources.collection.CollectionManager.page_size",
    "boto3.resources.collection.collectionmanager.pages": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/collections.html#boto3.resources.collection.CollectionManager.pages",
    "boto3.resources.collection.resourcecollection": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/collections.html#boto3.resources.collection.ResourceCollection",
    "boto3.resources.collection.resourcecollection.all": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/collections.html#boto3.resources.collection.ResourceCollection.all",
    "boto3.resources.collection.resourcecollection.filter": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/collections.html#boto3.resources.collection.ResourceCollection.filter",
    "boto3.resources.collection.resourcecollection.limit": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/collections.html#boto3.resources.collection.ResourceCollection.limit",
    "boto3.resources.collection.resourcecollection.page_size": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/collections.html#boto3.resources.collection.ResourceCollection.page_size",
    "boto3.resources.collection.resourcecollection.pages": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/collections.html#boto3.resources.collection.ResourceCollection.pages",
    "boto3.resources.factory": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/resources.html#module-boto3.resources.factory",
    "boto3.resources.factory.resourcefactory": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/resources.html#boto3.resources.factory.ResourceFactory",
    "boto3.resources.factory.resourcefactory.load_from_definition": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/resources.html#boto3.resources.factory.ResourceFactory.load_from_definition",
    "boto3.resources.model": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/resources.html#module-boto3.resources.model",
    "boto3.resources.model.action": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/resources.html#boto3.resources.model.Action",
    "boto3.resources.model.action.name": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/resources.html#boto3.resources.model.Action.name",
    "boto3.resources.model.action.path": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/resources.html#boto3.resources.model.Action.path",
    "boto3.resources.model.action.request": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/resources.html#boto3.resources.model.Action.request",
    "boto3.resources.model.action.resource": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/resources.html#boto3.resources.model.Action.resource",
    "boto3.resources.model.collection": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/resources.html#boto3.resources.model.Collection",
    "boto3.resources.model.collection.batch_actions": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/resources.html#boto3.resources.model.Collection.batch_actions",
    "boto3.resources.model.collection.name": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/resources.html#boto3.resources.model.Collection.name",
    "boto3.resources.model.collection.path": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/resources.html#boto3.resources.model.Collection.path",
    "boto3.resources.model.collection.request": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/resources.html#boto3.resources.model.Collection.request",
    "boto3.resources.model.collection.resource": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/resources.html#boto3.resources.model.Collection.resource",
    "boto3.resources.model.definitionwithparams": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/resources.html#boto3.resources.model.DefinitionWithParams",
    "boto3.resources.model.definitionwithparams.params": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/resources.html#boto3.resources.model.DefinitionWithParams.params",
    "boto3.resources.model.identifier": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/resources.html#boto3.resources.model.Identifier",
    "boto3.resources.model.identifier.name": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/resources.html#boto3.resources.model.Identifier.name",
    "boto3.resources.model.parameter": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/resources.html#boto3.resources.model.Parameter",
    "boto3.resources.model.parameter.name": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/resources.html#boto3.resources.model.Parameter.name",
    "boto3.resources.model.parameter.path": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/resources.html#boto3.resources.model.Parameter.path",
    "boto3.resources.model.parameter.source": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/resources.html#boto3.resources.model.Parameter.source",
    "boto3.resources.model.parameter.target": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/resources.html#boto3.resources.model.Parameter.target",
    "boto3.resources.model.parameter.value": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/resources.html#boto3.resources.model.Parameter.value",
    "boto3.resources.model.request": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/resources.html#boto3.resources.model.Request",
    "boto3.resources.model.request.operation": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/resources.html#boto3.resources.model.Request.operation",
    "boto3.resources.model.request.params": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/resources.html#boto3.resources.model.Request.params",
    "boto3.resources.model.resourcemodel": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/resources.html#boto3.resources.model.ResourceModel",
    "boto3.resources.model.resourcemodel.actions": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/resources.html#boto3.resources.model.ResourceModel.actions",
    "boto3.resources.model.resourcemodel.batch_actions": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/resources.html#boto3.resources.model.ResourceModel.batch_actions",
    "boto3.resources.model.resourcemodel.collections": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/resources.html#boto3.resources.model.ResourceModel.collections",
    "boto3.resources.model.resourcemodel.get_attributes": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/resources.html#boto3.resources.model.ResourceModel.get_attributes",
    "boto3.resources.model.resourcemodel.identifiers": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/resources.html#boto3.resources.model.ResourceModel.identifiers",
    "boto3.resources.model.resourcemodel.load": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/resources.html#boto3.resources.model.ResourceModel.load",
    "boto3.resources.model.resourcemodel.load_rename_map": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/resources.html#boto3.resources.model.ResourceModel.load_rename_map",
    "boto3.resources.model.resourcemodel.name": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/resources.html#boto3.resources.model.ResourceModel.name",
    "boto3.resources.model.resourcemodel.references": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/resources.html#boto3.resources.model.ResourceModel.references",
    "boto3.resources.model.resourcemodel.shape": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/resources.html#boto3.resources.model.ResourceModel.shape",
    "boto3.resources.model.resourcemodel.subresources": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/resources.html#boto3.resources.model.ResourceModel.subresources",
    "boto3.resources.model.resourcemodel.waiters": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/resources.html#boto3.resources.model.ResourceModel.waiters",
    "boto3.resources.model.responseresource": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/resources.html#boto3.resources.model.ResponseResource",
    "boto3.resources.model.responseresource.identifiers": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/resources.html#boto3.resources.model.ResponseResource.identifiers",
    "boto3.resources.model.responseresource.model": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/resources.html#boto3.resources.model.ResponseResource.model",
    "boto3.resources.model.responseresource.path": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/resources.html#boto3.resources.model.ResponseResource.path",
    "boto3.resources.model.responseresource.type": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/resources.html#boto3.resources.model.ResponseResource.type",
    "boto3.resources.model.waiter": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/resources.html#boto3.resources.model.Waiter",
    "boto3.resources.model.waiter.name": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/resources.html#boto3.resources.model.Waiter.name",
    "boto3.resources.model.waiter.params": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/resources.html#boto3.resources.model.Waiter.params",
    "boto3.resources.model.waiter.prefix": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/resources.html#boto3.resources.model.Waiter.PREFIX",
    "boto3.resources.model.waiter.waiter_name": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/resources.html#boto3.resources.model.Waiter.waiter_name",
    "boto3.resources.params": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/resources.html#module-boto3.resources.params",
    "boto3.resources.params.build_param_structure": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/resources.html#boto3.resources.params.build_param_structure",
    "boto3.resources.params.create_request_parameters": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/resources.html#boto3.resources.params.create_request_parameters",
    "boto3.resources.params.get_data_member": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/resources.html#boto3.resources.params.get_data_member",
    "boto3.resources.response": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/resources.html#module-boto3.resources.response",
    "boto3.resources.response.all_not_none": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/resources.html#boto3.resources.response.all_not_none",
    "boto3.resources.response.build_empty_response": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/resources.html#boto3.resources.response.build_empty_response",
    "boto3.resources.response.build_identifiers": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/resources.html#boto3.resources.response.build_identifiers",
    "boto3.resources.response.rawhandler": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/resources.html#boto3.resources.response.RawHandler",
    "boto3.resources.response.resourcehandler": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/resources.html#boto3.resources.response.ResourceHandler",
    "boto3.resources.response.resourcehandler.handle_response_item": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/resources.html#boto3.resources.response.ResourceHandler.handle_response_item",
    "boto3.s3": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/customizations/s3.html",
    "boto3.s3.transfer": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/customizations/s3.html",
    "boto3.s3.transfer.s3transfer": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/customizations/s3.html#boto3.s3.transfer.S3Transfer",
    "boto3.s3.transfer.s3transfer.allowed_download_args": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/customizations/s3.html#boto3.s3.transfer.S3Transfer.ALLOWED_DOWNLOAD_ARGS",
    "boto3.s3.transfer.s3transfer.allowed_upload_args": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/customizations/s3.html#boto3.s3.transfer.S3Transfer.ALLOWED_UPLOAD_ARGS",
    "boto3.s3.transfer.s3transfer.download_file": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/customizations/s3.html#boto3.s3.transfer.S3Transfer.download_file",
    "boto3.s3.transfer.s3transfer.upload_file": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/customizations/s3.html#boto3.s3.transfer.S3Transfer.upload_file",
    "boto3.s3.transfer.transferconfig": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/customizations/s3.html#boto3.s3.transfer.TransferConfig",
    "boto3.s3.transfer.transferconfig.alias": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/customizations/s3.html#boto3.s3.transfer.TransferConfig.ALIAS",
    "boto3.session": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/session.html",
    "boto3.session.session": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/session.html#boto3.session.Session",
    "boto3.session.session.available_profiles": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/session.html#boto3.session.Session.available_profiles",
    "boto3.session.session.client": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/session.html#boto3.session.Session.client",
    "boto3.session.session.events": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/session.html#boto3.session.Session.events",
    "boto3.session.session.get_available_partitions": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/session.html#boto3.session.Session.get_available_partitions",
    "boto3.session.session.get_available_regions": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/session.html#boto3.session.Session.get_available_regions",
    "boto3.session.session.get_available_resources": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/session.html#boto3.session.Session.get_available_resources",
    "boto3.session.session.get_available_services": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/session.html#boto3.session.Session.get_available_services",
    "boto3.session.session.get_credentials": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/session.html#boto3.session.Session.get_credentials",
    "boto3.session.session.get_partition_for_region": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/session.html#boto3.session.Session.get_partition_for_region",
    "boto3.session.session.profile_name": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/session.html#boto3.session.Session.profile_name",
    "boto3.session.session.region_name": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/session.html#boto3.session.Session.region_name",
    "boto3.session.session.resource": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/session.html#boto3.session.Session.resource",
    "boto3.set_stream_logger": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/boto3.html#boto3.set_stream_logger",
    "boto3.setup_default_session": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/boto3.html#boto3.setup_default_session",
}
