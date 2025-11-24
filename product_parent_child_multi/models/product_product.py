# Copyright 2020 ForgeFlow S.L. (https://forgeflow.com)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    child_ids = fields.Many2many('product.product', 'product_parent_product_child_rel',
                                 'parent_id', 'child_id',
                                 string='Child Products')
    child_count = fields.Integer(
        compute="_compute_child_count", string="Number of child products"
    )
    parent_ids = fields.Many2many('product.product', 'product_parent_product_child_rel',
                                  'child_id', 'parent_id',
                                  string='Parent Products')
    parent_count = fields.Integer(
        compute="_compute_parent_count", string="Number of parent products"
    )

    @api.depends("child_ids")
    def _compute_child_count(self):
        for product in self:
            product.child_count = len(product.child_ids)

    @api.depends("parent_ids")
    def _compute_parent_count(self):
        for product in self:
            product.parent_count = len(product.parent_ids)

    def preview_child_list(self):
        return {
            "name": self.env._("Child product of %s") % self.name,
            "type": "ir.actions.act_window",
            "res_model": "product.product",
            "view_mode": "list,form",
            "path": "child-products",
            "context": {
                **self.env.context,
                "default_parent_ids": self.id,
                "parent_ids_editable": False,
            },
            "domain": [("parent_ids", "in", self.id)],
        }

    def preview_parent_list(self):
        return {
            "name": self.env._("Parent product of %s") % self.name,
            "type": "ir.actions.act_window",
            "res_model": "product.product",
            "view_mode": "list,form",
            "path": "parent-products",
            "context": {
                **self.env.context,
                "default_child_ids": self.id,
                "child_ids_editable": False,
            },
            "domain": [("child_ids", "in", self.id)],
        }
