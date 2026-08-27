
    async def process_quantity(
        self, product_id: int, quantity_str: str
    ) -> ResponseProductDomain:
        try:
            quantity = Decimal(quantity_str)
        except InvalidOperation:
            return ResponseProductDomain(ProductInputResult.INVALID_QUANTITY)
        request = await self.repository.create_request(
            product_id,
            int(quantity),
        )
