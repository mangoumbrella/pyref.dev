VERSION = "2.7.5"

# fmt: off
MAPPING = {
    "django_tables2": "https://django-tables2.readthedocs.io/en/latest/",
    "django_tables2.columns.booleancolumn": "https://django-tables2.readthedocs.io/en/latest/pages/api-reference.html#django_tables2.columns.BooleanColumn",
    "django_tables2.columns.boundcolumn": "https://django-tables2.readthedocs.io/en/latest/pages/internal.html#django_tables2.columns.BoundColumn",
    "django_tables2.columns.boundcolumn.__init__": "https://django-tables2.readthedocs.io/en/latest/pages/internal.html#django_tables2.columns.BoundColumn.__init__",
    "django_tables2.columns.boundcolumn.__str__": "https://django-tables2.readthedocs.io/en/latest/pages/internal.html#django_tables2.columns.BoundColumn.__str__",
    "django_tables2.columns.boundcolumn.__weakref__": "https://django-tables2.readthedocs.io/en/latest/pages/internal.html#django_tables2.columns.BoundColumn.__weakref__",
    "django_tables2.columns.boundcolumn._get_cell_class": "https://django-tables2.readthedocs.io/en/latest/pages/internal.html#django_tables2.columns.BoundColumn._get_cell_class",
    "django_tables2.columns.boundcolumn.accessor": "https://django-tables2.readthedocs.io/en/latest/pages/internal.html#django_tables2.columns.BoundColumn.accessor",
    "django_tables2.columns.boundcolumn.attrs": "https://django-tables2.readthedocs.io/en/latest/pages/internal.html#django_tables2.columns.BoundColumn.attrs",
    "django_tables2.columns.boundcolumn.default": "https://django-tables2.readthedocs.io/en/latest/pages/internal.html#django_tables2.columns.BoundColumn.default",
    "django_tables2.columns.boundcolumn.footer": "https://django-tables2.readthedocs.io/en/latest/pages/internal.html#django_tables2.columns.BoundColumn.footer",
    "django_tables2.columns.boundcolumn.get_td_class": "https://django-tables2.readthedocs.io/en/latest/pages/internal.html#django_tables2.columns.BoundColumn.get_td_class",
    "django_tables2.columns.boundcolumn.get_th_class": "https://django-tables2.readthedocs.io/en/latest/pages/internal.html#django_tables2.columns.BoundColumn.get_th_class",
    "django_tables2.columns.boundcolumn.header": "https://django-tables2.readthedocs.io/en/latest/pages/internal.html#django_tables2.columns.BoundColumn.header",
    "django_tables2.columns.boundcolumn.localize": "https://django-tables2.readthedocs.io/en/latest/pages/internal.html#django_tables2.columns.BoundColumn.localize",
    "django_tables2.columns.boundcolumn.order_by": "https://django-tables2.readthedocs.io/en/latest/pages/internal.html#django_tables2.columns.BoundColumn.order_by",
    "django_tables2.columns.boundcolumn.order_by_alias": "https://django-tables2.readthedocs.io/en/latest/pages/internal.html#django_tables2.columns.BoundColumn.order_by_alias",
    "django_tables2.columns.boundcolumn.orderable": "https://django-tables2.readthedocs.io/en/latest/pages/internal.html#django_tables2.columns.BoundColumn.orderable",
    "django_tables2.columns.boundcolumn.verbose_name": "https://django-tables2.readthedocs.io/en/latest/pages/internal.html#django_tables2.columns.BoundColumn.verbose_name",
    "django_tables2.columns.boundcolumn.visible": "https://django-tables2.readthedocs.io/en/latest/pages/internal.html#django_tables2.columns.BoundColumn.visible",
    "django_tables2.columns.boundcolumns": "https://django-tables2.readthedocs.io/en/latest/pages/internal.html#django_tables2.columns.BoundColumns",
    "django_tables2.columns.boundcolumns.__contains__": "https://django-tables2.readthedocs.io/en/latest/pages/internal.html#django_tables2.columns.BoundColumns.__contains__",
    "django_tables2.columns.boundcolumns.__getitem__": "https://django-tables2.readthedocs.io/en/latest/pages/internal.html#django_tables2.columns.BoundColumns.__getitem__",
    "django_tables2.columns.boundcolumns.__init__": "https://django-tables2.readthedocs.io/en/latest/pages/internal.html#django_tables2.columns.BoundColumns.__init__",
    "django_tables2.columns.boundcolumns.__iter__": "https://django-tables2.readthedocs.io/en/latest/pages/internal.html#django_tables2.columns.BoundColumns.__iter__",
    "django_tables2.columns.boundcolumns.__len__": "https://django-tables2.readthedocs.io/en/latest/pages/internal.html#django_tables2.columns.BoundColumns.__len__",
    "django_tables2.columns.boundcolumns.__weakref__": "https://django-tables2.readthedocs.io/en/latest/pages/internal.html#django_tables2.columns.BoundColumns.__weakref__",
    "django_tables2.columns.boundcolumns.hide": "https://django-tables2.readthedocs.io/en/latest/pages/internal.html#django_tables2.columns.BoundColumns.hide",
    "django_tables2.columns.boundcolumns.iterall": "https://django-tables2.readthedocs.io/en/latest/pages/internal.html#django_tables2.columns.BoundColumns.iterall",
    "django_tables2.columns.boundcolumns.iteritems": "https://django-tables2.readthedocs.io/en/latest/pages/internal.html#django_tables2.columns.BoundColumns.iteritems",
    "django_tables2.columns.boundcolumns.iterorderable": "https://django-tables2.readthedocs.io/en/latest/pages/internal.html#django_tables2.columns.BoundColumns.iterorderable",
    "django_tables2.columns.boundcolumns.itervisible": "https://django-tables2.readthedocs.io/en/latest/pages/internal.html#django_tables2.columns.BoundColumns.itervisible",
    "django_tables2.columns.boundcolumns.show": "https://django-tables2.readthedocs.io/en/latest/pages/internal.html#django_tables2.columns.BoundColumns.show",
    "django_tables2.columns.checkboxcolumn": "https://django-tables2.readthedocs.io/en/latest/pages/api-reference.html#django_tables2.columns.CheckBoxColumn",
    "django_tables2.columns.checkboxcolumn.header": "https://django-tables2.readthedocs.io/en/latest/pages/api-reference.html#django_tables2.columns.CheckBoxColumn.header",
    "django_tables2.columns.checkboxcolumn.is_checked": "https://django-tables2.readthedocs.io/en/latest/pages/api-reference.html#django_tables2.columns.CheckBoxColumn.is_checked",
    "django_tables2.columns.checkboxcolumn.render": "https://django-tables2.readthedocs.io/en/latest/pages/api-reference.html#django_tables2.columns.CheckBoxColumn.render",
    "django_tables2.columns.column": "https://django-tables2.readthedocs.io/en/latest/pages/api-reference.html#django_tables2.columns.Column",
    "django_tables2.columns.column.order": "https://django-tables2.readthedocs.io/en/latest/pages/api-reference.html#django_tables2.columns.Column.order",
    "django_tables2.columns.column.render": "https://django-tables2.readthedocs.io/en/latest/pages/api-reference.html#django_tables2.columns.Column.render",
    "django_tables2.columns.column.value": "https://django-tables2.readthedocs.io/en/latest/pages/api-reference.html#django_tables2.columns.Column.value",
    "django_tables2.columns.datecolumn": "https://django-tables2.readthedocs.io/en/latest/pages/api-reference.html#django_tables2.columns.DateColumn",
    "django_tables2.columns.datecolumn.from_field": "https://django-tables2.readthedocs.io/en/latest/pages/api-reference.html#django_tables2.columns.DateColumn.from_field",
    "django_tables2.columns.datetimecolumn": "https://django-tables2.readthedocs.io/en/latest/pages/api-reference.html#django_tables2.columns.DateTimeColumn",
    "django_tables2.columns.datetimecolumn.from_field": "https://django-tables2.readthedocs.io/en/latest/pages/api-reference.html#django_tables2.columns.DateTimeColumn.from_field",
    "django_tables2.columns.emailcolumn": "https://django-tables2.readthedocs.io/en/latest/pages/api-reference.html#django_tables2.columns.EmailColumn",
    "django_tables2.columns.emailcolumn.from_field": "https://django-tables2.readthedocs.io/en/latest/pages/api-reference.html#django_tables2.columns.EmailColumn.from_field",
    "django_tables2.columns.filecolumn": "https://django-tables2.readthedocs.io/en/latest/pages/api-reference.html#django_tables2.columns.FileColumn",
    "django_tables2.columns.filecolumn.from_field": "https://django-tables2.readthedocs.io/en/latest/pages/api-reference.html#django_tables2.columns.FileColumn.from_field",
    "django_tables2.columns.filecolumn.render": "https://django-tables2.readthedocs.io/en/latest/pages/api-reference.html#django_tables2.columns.FileColumn.render",
    "django_tables2.columns.jsoncolumn": "https://django-tables2.readthedocs.io/en/latest/pages/api-reference.html#django_tables2.columns.JSONColumn",
    "django_tables2.columns.jsoncolumn.from_field": "https://django-tables2.readthedocs.io/en/latest/pages/api-reference.html#django_tables2.columns.JSONColumn.from_field",
    "django_tables2.columns.jsoncolumn.render": "https://django-tables2.readthedocs.io/en/latest/pages/api-reference.html#django_tables2.columns.JSONColumn.render",
    "django_tables2.columns.linkcolumn": "https://django-tables2.readthedocs.io/en/latest/pages/api-reference.html#django_tables2.columns.LinkColumn",
    "django_tables2.columns.manytomanycolumn": "https://django-tables2.readthedocs.io/en/latest/pages/api-reference.html#django_tables2.columns.ManyToManyColumn",
    "django_tables2.columns.manytomanycolumn.filter": "https://django-tables2.readthedocs.io/en/latest/pages/api-reference.html#django_tables2.columns.ManyToManyColumn.filter",
    "django_tables2.columns.manytomanycolumn.from_field": "https://django-tables2.readthedocs.io/en/latest/pages/api-reference.html#django_tables2.columns.ManyToManyColumn.from_field",
    "django_tables2.columns.manytomanycolumn.render": "https://django-tables2.readthedocs.io/en/latest/pages/api-reference.html#django_tables2.columns.ManyToManyColumn.render",
    "django_tables2.columns.manytomanycolumn.transform": "https://django-tables2.readthedocs.io/en/latest/pages/api-reference.html#django_tables2.columns.ManyToManyColumn.transform",
    "django_tables2.columns.relatedlinkcolumn": "https://django-tables2.readthedocs.io/en/latest/pages/api-reference.html#django_tables2.columns.RelatedLinkColumn",
    "django_tables2.columns.templatecolumn": "https://django-tables2.readthedocs.io/en/latest/pages/api-reference.html#django_tables2.columns.TemplateColumn",
    "django_tables2.columns.templatecolumn.render": "https://django-tables2.readthedocs.io/en/latest/pages/api-reference.html#django_tables2.columns.TemplateColumn.render",
    "django_tables2.columns.templatecolumn.value": "https://django-tables2.readthedocs.io/en/latest/pages/api-reference.html#django_tables2.columns.TemplateColumn.value",
    "django_tables2.columns.urlcolumn": "https://django-tables2.readthedocs.io/en/latest/pages/api-reference.html#django_tables2.columns.URLColumn",
    "django_tables2.columns.urlcolumn.from_field": "https://django-tables2.readthedocs.io/en/latest/pages/api-reference.html#django_tables2.columns.URLColumn.from_field",
    "django_tables2.config": "https://django-tables2.readthedocs.io/en/latest/pages/api-reference.html",
    "django_tables2.config.requestconfig": "https://django-tables2.readthedocs.io/en/latest/pages/api-reference.html#django_tables2.config.RequestConfig",
    "django_tables2.export": "https://django-tables2.readthedocs.io/en/latest/pages/api-reference.html",
    "django_tables2.export.exportmixin": "https://django-tables2.readthedocs.io/en/latest/pages/api-reference.html#django_tables2.export.ExportMixin",
    "django_tables2.export.exportmixin.dataset_kwargs": "https://django-tables2.readthedocs.io/en/latest/pages/api-reference.html#django_tables2.export.ExportMixin.dataset_kwargs",
    "django_tables2.export.exportmixin.exclude_columns": "https://django-tables2.readthedocs.io/en/latest/pages/api-reference.html#django_tables2.export.ExportMixin.exclude_columns",
    "django_tables2.export.exportmixin.export_class": "https://django-tables2.readthedocs.io/en/latest/pages/api-reference.html#django_tables2.export.ExportMixin.export_class",
    "django_tables2.export.exportmixin.export_formats": "https://django-tables2.readthedocs.io/en/latest/pages/api-reference.html#django_tables2.export.ExportMixin.export_formats",
    "django_tables2.export.exportmixin.export_name": "https://django-tables2.readthedocs.io/en/latest/pages/api-reference.html#django_tables2.export.ExportMixin.export_name",
    "django_tables2.export.exportmixin.export_trigger_param": "https://django-tables2.readthedocs.io/en/latest/pages/api-reference.html#django_tables2.export.ExportMixin.export_trigger_param",
    "django_tables2.export.tableexport": "https://django-tables2.readthedocs.io/en/latest/pages/api-reference.html#django_tables2.export.TableExport",
    "django_tables2.export.tableexport.content_type": "https://django-tables2.readthedocs.io/en/latest/pages/api-reference.html#django_tables2.export.TableExport.content_type",
    "django_tables2.export.tableexport.export": "https://django-tables2.readthedocs.io/en/latest/pages/api-reference.html#django_tables2.export.TableExport.export",
    "django_tables2.export.tableexport.is_valid_format": "https://django-tables2.readthedocs.io/en/latest/pages/api-reference.html#django_tables2.export.TableExport.is_valid_format",
    "django_tables2.export.tableexport.response": "https://django-tables2.readthedocs.io/en/latest/pages/api-reference.html#django_tables2.export.TableExport.response",
    "django_tables2.export.tableexport.table_to_dataset": "https://django-tables2.readthedocs.io/en/latest/pages/api-reference.html#django_tables2.export.TableExport.table_to_dataset",
    "django_tables2.paginators": "https://django-tables2.readthedocs.io/en/latest/pages/api-reference.html",
    "django_tables2.paginators.lazypaginator": "https://django-tables2.readthedocs.io/en/latest/pages/api-reference.html#django_tables2.paginators.LazyPaginator",
    "django_tables2.rows": "https://django-tables2.readthedocs.io/en/latest/pages/internal.html",
    "django_tables2.rows.boundpinnedrow": "https://django-tables2.readthedocs.io/en/latest/pages/internal.html#django_tables2.rows.BoundPinnedRow",
    "django_tables2.rows.boundpinnedrow.attrs": "https://django-tables2.readthedocs.io/en/latest/pages/internal.html#django_tables2.rows.BoundPinnedRow.attrs",
    "django_tables2.rows.boundrow": "https://django-tables2.readthedocs.io/en/latest/pages/internal.html#django_tables2.rows.BoundRow",
    "django_tables2.rows.boundrow.__contains__": "https://django-tables2.readthedocs.io/en/latest/pages/internal.html#django_tables2.rows.BoundRow.__contains__",
    "django_tables2.rows.boundrow.__init__": "https://django-tables2.readthedocs.io/en/latest/pages/internal.html#django_tables2.rows.BoundRow.__init__",
    "django_tables2.rows.boundrow.__iter__": "https://django-tables2.readthedocs.io/en/latest/pages/internal.html#django_tables2.rows.BoundRow.__iter__",
    "django_tables2.rows.boundrow.__weakref__": "https://django-tables2.readthedocs.io/en/latest/pages/internal.html#django_tables2.rows.BoundRow.__weakref__",
    "django_tables2.rows.boundrow._call_render": "https://django-tables2.readthedocs.io/en/latest/pages/internal.html#django_tables2.rows.BoundRow._call_render",
    "django_tables2.rows.boundrow._call_value": "https://django-tables2.readthedocs.io/en/latest/pages/internal.html#django_tables2.rows.BoundRow._call_value",
    "django_tables2.rows.boundrow._optional_cell_arguments": "https://django-tables2.readthedocs.io/en/latest/pages/internal.html#django_tables2.rows.BoundRow._optional_cell_arguments",
    "django_tables2.rows.boundrow.attrs": "https://django-tables2.readthedocs.io/en/latest/pages/internal.html#django_tables2.rows.BoundRow.attrs",
    "django_tables2.rows.boundrow.get_cell": "https://django-tables2.readthedocs.io/en/latest/pages/internal.html#django_tables2.rows.BoundRow.get_cell",
    "django_tables2.rows.boundrow.get_cell_value": "https://django-tables2.readthedocs.io/en/latest/pages/internal.html#django_tables2.rows.BoundRow.get_cell_value",
    "django_tables2.rows.boundrow.get_even_odd_css_class": "https://django-tables2.readthedocs.io/en/latest/pages/internal.html#django_tables2.rows.BoundRow.get_even_odd_css_class",
    "django_tables2.rows.boundrow.items": "https://django-tables2.readthedocs.io/en/latest/pages/internal.html#django_tables2.rows.BoundRow.items",
    "django_tables2.rows.boundrow.record": "https://django-tables2.readthedocs.io/en/latest/pages/internal.html#django_tables2.rows.BoundRow.record",
    "django_tables2.rows.boundrow.table": "https://django-tables2.readthedocs.io/en/latest/pages/internal.html#django_tables2.rows.BoundRow.table",
    "django_tables2.rows.boundrows": "https://django-tables2.readthedocs.io/en/latest/pages/internal.html#django_tables2.rows.BoundRows",
    "django_tables2.rows.boundrows.__getitem__": "https://django-tables2.readthedocs.io/en/latest/pages/internal.html#django_tables2.rows.BoundRows.__getitem__",
    "django_tables2.rows.boundrows.__init__": "https://django-tables2.readthedocs.io/en/latest/pages/internal.html#django_tables2.rows.BoundRows.__init__",
    "django_tables2.rows.boundrows.__weakref__": "https://django-tables2.readthedocs.io/en/latest/pages/internal.html#django_tables2.rows.BoundRows.__weakref__",
    "django_tables2.rows.boundrows.generator_pinned_row": "https://django-tables2.readthedocs.io/en/latest/pages/internal.html#django_tables2.rows.BoundRows.generator_pinned_row",
    "django_tables2.tables.table": "https://django-tables2.readthedocs.io/en/latest/pages/api-reference.html#django_tables2.tables.Table",
    "django_tables2.tables.table.as_html": "https://django-tables2.readthedocs.io/en/latest/pages/api-reference.html#django_tables2.tables.Table.as_html",
    "django_tables2.tables.table.as_values": "https://django-tables2.readthedocs.io/en/latest/pages/api-reference.html#django_tables2.tables.Table.as_values",
    "django_tables2.tables.table.before_render": "https://django-tables2.readthedocs.io/en/latest/pages/api-reference.html#django_tables2.tables.Table.before_render",
    "django_tables2.tables.table.get_bottom_pinned_data": "https://django-tables2.readthedocs.io/en/latest/pages/api-reference.html#django_tables2.tables.Table.get_bottom_pinned_data",
    "django_tables2.tables.table.get_column_class_names": "https://django-tables2.readthedocs.io/en/latest/pages/api-reference.html#django_tables2.tables.Table.get_column_class_names",
    "django_tables2.tables.table.get_top_pinned_data": "https://django-tables2.readthedocs.io/en/latest/pages/api-reference.html#django_tables2.tables.Table.get_top_pinned_data",
    "django_tables2.tables.table.paginate": "https://django-tables2.readthedocs.io/en/latest/pages/api-reference.html#django_tables2.tables.Table.paginate",
    "django_tables2.tables.tabledata": "https://django-tables2.readthedocs.io/en/latest/pages/internal.html#django_tables2.tables.TableData",
    "django_tables2.tables.tabledata.__getitem__": "https://django-tables2.readthedocs.io/en/latest/pages/internal.html#django_tables2.tables.TableData.__getitem__",
    "django_tables2.tables.tabledata.__init__": "https://django-tables2.readthedocs.io/en/latest/pages/internal.html#django_tables2.tables.TableData.__init__",
    "django_tables2.tables.tabledata.__iter__": "https://django-tables2.readthedocs.io/en/latest/pages/internal.html#django_tables2.tables.TableData.__iter__",
    "django_tables2.tables.tabledata.__weakref__": "https://django-tables2.readthedocs.io/en/latest/pages/internal.html#django_tables2.tables.TableData.__weakref__",
    "django_tables2.tables.tabledata.set_table": "https://django-tables2.readthedocs.io/en/latest/pages/internal.html#django_tables2.tables.TableData.set_table",
    "django_tables2.utils.accessor": "https://django-tables2.readthedocs.io/en/latest/pages/api-reference.html#django_tables2.utils.Accessor",
    "django_tables2.utils.orderby": "https://django-tables2.readthedocs.io/en/latest/pages/internal.html#django_tables2.utils.OrderBy",
    "django_tables2.utils.orderby.__new__": "https://django-tables2.readthedocs.io/en/latest/pages/internal.html#django_tables2.utils.OrderBy.__new__",
    "django_tables2.utils.orderby.__weakref__": "https://django-tables2.readthedocs.io/en/latest/pages/internal.html#django_tables2.utils.OrderBy.__weakref__",
    "django_tables2.utils.orderby.bare": "https://django-tables2.readthedocs.io/en/latest/pages/internal.html#django_tables2.utils.OrderBy.bare",
    "django_tables2.utils.orderby.for_queryset": "https://django-tables2.readthedocs.io/en/latest/pages/internal.html#django_tables2.utils.OrderBy.for_queryset",
    "django_tables2.utils.orderby.is_ascending": "https://django-tables2.readthedocs.io/en/latest/pages/internal.html#django_tables2.utils.OrderBy.is_ascending",
    "django_tables2.utils.orderby.is_descending": "https://django-tables2.readthedocs.io/en/latest/pages/internal.html#django_tables2.utils.OrderBy.is_descending",
    "django_tables2.utils.orderby.opposite": "https://django-tables2.readthedocs.io/en/latest/pages/internal.html#django_tables2.utils.OrderBy.opposite",
    "django_tables2.utils.orderbytuple": "https://django-tables2.readthedocs.io/en/latest/pages/internal.html#django_tables2.utils.OrderByTuple",
    "django_tables2.utils.orderbytuple.__contains__": "https://django-tables2.readthedocs.io/en/latest/pages/internal.html#django_tables2.utils.OrderByTuple.__contains__",
    "django_tables2.utils.orderbytuple.__getitem__": "https://django-tables2.readthedocs.io/en/latest/pages/internal.html#django_tables2.utils.OrderByTuple.__getitem__",
    "django_tables2.utils.orderbytuple.__new__": "https://django-tables2.readthedocs.io/en/latest/pages/internal.html#django_tables2.utils.OrderByTuple.__new__",
    "django_tables2.utils.orderbytuple.__str__": "https://django-tables2.readthedocs.io/en/latest/pages/internal.html#django_tables2.utils.OrderByTuple.__str__",
    "django_tables2.utils.orderbytuple.get": "https://django-tables2.readthedocs.io/en/latest/pages/internal.html#django_tables2.utils.OrderByTuple.get",
    "django_tables2.utils.orderbytuple.opposite": "https://django-tables2.readthedocs.io/en/latest/pages/internal.html#django_tables2.utils.OrderByTuple.opposite",
    "django_tables2.utils.sequence": "https://django-tables2.readthedocs.io/en/latest/pages/internal.html#django_tables2.utils.Sequence",
    "django_tables2.utils.sequence.__weakref__": "https://django-tables2.readthedocs.io/en/latest/pages/internal.html#django_tables2.utils.Sequence.__weakref__",
    "django_tables2.utils.sequence.expand": "https://django-tables2.readthedocs.io/en/latest/pages/internal.html#django_tables2.utils.Sequence.expand",
    "django_tables2.views": "https://django-tables2.readthedocs.io/en/latest/pages/api-reference.html",
    "django_tables2.views.multitablemixin": "https://django-tables2.readthedocs.io/en/latest/pages/api-reference.html#django_tables2.views.MultiTableMixin",
    "django_tables2.views.multitablemixin.context_table_name": "https://django-tables2.readthedocs.io/en/latest/pages/api-reference.html#django_tables2.views.MultiTableMixin.context_table_name",
    "django_tables2.views.multitablemixin.get_tables": "https://django-tables2.readthedocs.io/en/latest/pages/api-reference.html#django_tables2.views.MultiTableMixin.get_tables",
    "django_tables2.views.multitablemixin.get_tables_data": "https://django-tables2.readthedocs.io/en/latest/pages/api-reference.html#django_tables2.views.MultiTableMixin.get_tables_data",
    "django_tables2.views.multitablemixin.table_prefix": "https://django-tables2.readthedocs.io/en/latest/pages/api-reference.html#django_tables2.views.MultiTableMixin.table_prefix",
    "django_tables2.views.multitablemixin.tables": "https://django-tables2.readthedocs.io/en/latest/pages/api-reference.html#django_tables2.views.MultiTableMixin.tables",
    "django_tables2.views.multitablemixin.tables_data": "https://django-tables2.readthedocs.io/en/latest/pages/api-reference.html#django_tables2.views.MultiTableMixin.tables_data",
    "django_tables2.views.singletablemixin": "https://django-tables2.readthedocs.io/en/latest/pages/api-reference.html#django_tables2.views.SingleTableMixin",
    "django_tables2.views.singletablemixin.context_table_name": "https://django-tables2.readthedocs.io/en/latest/pages/api-reference.html#django_tables2.views.SingleTableMixin.context_table_name",
    "django_tables2.views.singletablemixin.get_context_data": "https://django-tables2.readthedocs.io/en/latest/pages/api-reference.html#django_tables2.views.SingleTableMixin.get_context_data",
    "django_tables2.views.singletablemixin.get_table": "https://django-tables2.readthedocs.io/en/latest/pages/api-reference.html#django_tables2.views.SingleTableMixin.get_table",
    "django_tables2.views.singletablemixin.get_table_class": "https://django-tables2.readthedocs.io/en/latest/pages/api-reference.html#django_tables2.views.SingleTableMixin.get_table_class",
    "django_tables2.views.singletablemixin.get_table_data": "https://django-tables2.readthedocs.io/en/latest/pages/api-reference.html#django_tables2.views.SingleTableMixin.get_table_data",
    "django_tables2.views.singletablemixin.get_table_kwargs": "https://django-tables2.readthedocs.io/en/latest/pages/api-reference.html#django_tables2.views.SingleTableMixin.get_table_kwargs",
    "django_tables2.views.singletablemixin.table_class": "https://django-tables2.readthedocs.io/en/latest/pages/api-reference.html#django_tables2.views.SingleTableMixin.table_class",
    "django_tables2.views.singletablemixin.table_data": "https://django-tables2.readthedocs.io/en/latest/pages/api-reference.html#django_tables2.views.SingleTableMixin.table_data",
    "django_tables2.views.singletablemixin.table_pagination": "https://django-tables2.readthedocs.io/en/latest/pages/api-reference.html#django_tables2.views.SingleTableMixin.table_pagination",
    "django_tables2.views.singletableview": "https://django-tables2.readthedocs.io/en/latest/pages/api-reference.html#django_tables2.views.SingleTableView",
    "django_tables2.views.singletableview.get_table": "https://django-tables2.readthedocs.io/en/latest/pages/api-reference.html#django_tables2.views.SingleTableView.get_table",
    "django_tables2.views.singletableview.get_table_kwargs": "https://django-tables2.readthedocs.io/en/latest/pages/api-reference.html#django_tables2.views.SingleTableView.get_table_kwargs",
}
