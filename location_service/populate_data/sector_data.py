"""
Script para poblar las tablas relacionadas con sectores
"""
from datetime import datetime
from commons.database import db_manager
from infrastructure.models.measurement_unit import MeasurementUnit
from infrastructure.models.sector_type import SectorType
from infrastructure.models.ramp import Ramp
from infrastructure.models.sector import Sector
from infrastructure.models.branch import Branch
from domain.entities.measurement_unit import MeasurementUnit as MeasurementUnitEnum
from sqlalchemy.ext.asyncio import AsyncSession

async def populate_measurement_units(dry_run: bool = False):
    """Poblar unidades de medida"""
    print("📏 Poblando unidades de medida...")
    if dry_run:
        print("🔍 MODO SIMULACIÓN: No se guardarán datos en la BD")

    session: AsyncSession = await db_manager.get_session()
    try:
        # Datos de unidades de medida basados en el enum MeasurementUnit
        measurement_units = [
            MeasurementUnit(
                name="Palet",
                code="PALLET",
                description="Mercancía en palets",
                is_active=True,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            ),
            MeasurementUnit(
                name="Granel",
                code="GRANEL",
                description="Mercancía a granel",
                is_active=True,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            ),
            MeasurementUnit(
                name="Palet/Granel",
                code="PALLET_GRANEL",
                description="Mercancía mixta (palets y granel)",
                is_active=True,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            ),
        ]

        if not dry_run:
            for unit in measurement_units:
                session.add(unit)
            await session.commit()
            for unit in measurement_units:
                await session.refresh(unit)
                print(f"✅ Unidad de medida creada: {unit.name} (ID: {unit.id})")
        else:
            print(f"🔍 Simulación: {len(measurement_units)} unidades de medida a crear")
        
        return {"measurement_units": len(measurement_units)}
    except Exception as e:
        print(f"❌ Error poblando unidades de medida: {e}")
        if not dry_run:
            await session.rollback()
        raise
    finally:
        await session.close()

async def populate_sector_types(dry_run: bool = False):
    """Poblar tipos de sector"""
    print("🏭 Poblando tipos de sector...")
    if dry_run:
        print("🔍 MODO SIMULACIÓN: No se guardarán datos en la BD")

    session: AsyncSession = await db_manager.get_session()
    try:
        # Datos de tipos de sector basados en CSV proporcionado
        sector_types = [
            SectorType(name="Bazar", code="BAZAR", description="Productos de bazar", measurement_unit=MeasurementUnitEnum.PALLET, is_active=True, created_at=datetime.utcnow(), updated_at=datetime.utcnow()),
            SectorType(name="Bebés", code="BEBES", description="Productos para bebés", measurement_unit=MeasurementUnitEnum.PALLET, is_active=True, created_at=datetime.utcnow(), updated_at=datetime.utcnow()),
            SectorType(name="Bebidas", code="BEBIDAS", description="Bebidas y refrescos", measurement_unit=MeasurementUnitEnum.PALLET, is_active=True, created_at=datetime.utcnow(), updated_at=datetime.utcnow()),
            SectorType(name="Cárnicos", code="CARNICOS", description="Productos cárnicos", measurement_unit=MeasurementUnitEnum.PALLET, is_active=True, created_at=datetime.utcnow(), updated_at=datetime.utcnow()),
            SectorType(name="Cocina", code="COCINA", description="Productos de cocina", measurement_unit=MeasurementUnitEnum.PALLET, is_active=True, created_at=datetime.utcnow(), updated_at=datetime.utcnow()),
            SectorType(name="Cotillón", code="COTILLON", description="Productos de cotillón", measurement_unit=MeasurementUnitEnum.PALLET, is_active=True, created_at=datetime.utcnow(), updated_at=datetime.utcnow()),
            SectorType(name="Descartable", code="DESCARTABLE", description="Productos descartables", measurement_unit=MeasurementUnitEnum.PALLET, is_active=True, created_at=datetime.utcnow(), updated_at=datetime.utcnow()),
            SectorType(name="Ferretería", code="FERRETERIA", description="Productos de ferretería", measurement_unit=MeasurementUnitEnum.PALLET, is_active=True, created_at=datetime.utcnow(), updated_at=datetime.utcnow()),
            SectorType(name="FLV", code="FLV", description="Frutas, legumbres y verduras", measurement_unit=MeasurementUnitEnum.GRANEL, is_active=True, created_at=datetime.utcnow(), updated_at=datetime.utcnow()),
            SectorType(name="Fríos", code="FRIOS", description="Productos refrigerados", measurement_unit=MeasurementUnitEnum.PALLET_GRANEL, is_active=True, created_at=datetime.utcnow(), updated_at=datetime.utcnow()),
            SectorType(name="Golosina", code="GOLOSINA", description="Golosinas y dulces", measurement_unit=MeasurementUnitEnum.PALLET, is_active=True, created_at=datetime.utcnow(), updated_at=datetime.utcnow()),
            SectorType(name="Higiene", code="HIGIENE", description="Productos de higiene personal", measurement_unit=MeasurementUnitEnum.PALLET, is_active=True, created_at=datetime.utcnow(), updated_at=datetime.utcnow()),
            SectorType(name="Hogar", code="HOGAR", description="Productos para el hogar", measurement_unit=MeasurementUnitEnum.PALLET, is_active=True, created_at=datetime.utcnow(), updated_at=datetime.utcnow()),
            SectorType(name="Insumos", code="INSUMOS", description="Insumos varios", measurement_unit=MeasurementUnitEnum.PALLET, is_active=True, created_at=datetime.utcnow(), updated_at=datetime.utcnow()),
            SectorType(name="Lácteos", code="LACTEOS", description="Productos lácteos", measurement_unit=MeasurementUnitEnum.PALLET_GRANEL, is_active=True, created_at=datetime.utcnow(), updated_at=datetime.utcnow()),
            SectorType(name="Limpieza", code="LIMPIEZA", description="Productos de limpieza", measurement_unit=MeasurementUnitEnum.PALLET, is_active=True, created_at=datetime.utcnow(), updated_at=datetime.utcnow()),
            SectorType(name="Matinal", code="MATINAL", description="Productos para el desayuno", measurement_unit=MeasurementUnitEnum.PALLET, is_active=True, created_at=datetime.utcnow(), updated_at=datetime.utcnow()),
            SectorType(name="Panadería", code="PANADERIA", description="Productos de panadería", measurement_unit=MeasurementUnitEnum.PALLET, is_active=True, created_at=datetime.utcnow(), updated_at=datetime.utcnow()),
            SectorType(name="PET", code="PET", description="Productos PET", measurement_unit=MeasurementUnitEnum.PALLET, is_active=True, created_at=datetime.utcnow(), updated_at=datetime.utcnow()),
            SectorType(name="Repostería", code="REPOSTERIA", description="Productos de repostería", measurement_unit=MeasurementUnitEnum.PALLET, is_active=True, created_at=datetime.utcnow(), updated_at=datetime.utcnow()),
            SectorType(name="Tabaquería", code="TABAQUERIA", description="Productos de tabaquería", measurement_unit=MeasurementUnitEnum.PALLET, is_active=True, created_at=datetime.utcnow(), updated_at=datetime.utcnow()),
            SectorType(name="Tradicional", code="TRADICIONAL", description="Productos tradicionales", measurement_unit=MeasurementUnitEnum.PALLET_GRANEL, is_active=True, created_at=datetime.utcnow(), updated_at=datetime.utcnow()),
        ]

        if not dry_run:
            for sector_type in sector_types:
                session.add(sector_type)
            await session.commit()
            for sector_type in sector_types:
                await session.refresh(sector_type)
                print(f"✅ Tipo de sector creado: {sector_type.name} (ID: {sector_type.id})")
        else:
            print(f"🔍 Simulación: {len(sector_types)} tipos de sector a crear")
        
        return {"sector_types": len(sector_types)}
    except Exception as e:
        print(f"❌ Error poblando tipos de sector: {e}")
        if not dry_run:
            await session.rollback()
        raise
    finally:
        await session.close()

async def populate_sectors(dry_run: bool = False):
    """Poblar sectores: cada branch tendrá todos los sectores definidos en SectorType"""
    print("🏭 Poblando sectores...")
    if dry_run:
        print("🔍 MODO SIMULACIÓN: No se guardarán datos en la BD")

    session: AsyncSession = await db_manager.get_session()
    try:
        # Obtener todas las sucursales y tipos de sector
        branches_result = await session.execute(Branch.__table__.select())
        branches = branches_result.fetchall()
        sector_types_result = await session.execute(SectorType.__table__.select())
        sector_types = sector_types_result.fetchall()
        
        sectors = []
        for branch in branches:
            for sector_type in sector_types:
                sector = Sector(
                    name=f"{sector_type.name} - {branch.name}",
                    description=f"Sector {sector_type.name} en sucursal {branch.name}",
                    branch_id=branch.id,
                    sector_type_id=sector_type.id,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow(),
                )
                sectors.append(sector)
                if not dry_run:
                    session.add(sector)
        if not dry_run:
            await session.commit()
            for sector in sectors:
                await session.refresh(sector)
                print(f"✅ Sector creado: {sector.name} (ID: {sector.id})")
        else:
            for sector in sectors:
                print(f"🔍 Simulación: Sector a crear -> {sector.name} (Branch: {sector.branch_id}, SectorType: {sector.sector_type_id})")
        return {"sectors": len(sectors)}
    except Exception as e:
        print(f"❌ Error poblando sectores: {e}")
        if not dry_run:
            await session.rollback()
        raise
    finally:
        await session.close()

async def populate_sector_data(dry_run: bool = False):
    """Función principal para poblar todas las tablas relacionadas con sectores"""
    print("🏭 Iniciando población de datos de sectores...")
    if dry_run:
        print("🔍 MODO SIMULACIÓN: No se guardarán datos en la BD")

    try:
        # Poblar unidades de medida
        measurement_units_result = await populate_measurement_units(dry_run)
        
        # Poblar tipos de sector
        sector_types_result = await populate_sector_types(dry_run)
        
        # Poblar sectores
        sectors_result = await populate_sectors(dry_run)
        
        if dry_run:
            print(f"\n🔍 SIMULACIÓN COMPLETADA - No se guardaron datos")
        else:
            print(f"\n🎉 ¡Población de sectores completada exitosamente!")
        
        print(f"📊 Resumen de sectores:")
        print(f"   📏 Unidades de medida: {measurement_units_result['measurement_units']}")
        print(f"   🏭 Tipos de sector: {sector_types_result['sector_types']}")
        print(f"   🏭 Sectores: {sectors_result['sectors']}")
        
        return {
            "measurement_units": measurement_units_result["measurement_units"],
            "sector_types": sector_types_result["sector_types"],
            "sectors": sectors_result["sectors"]
        }
        
    except Exception as e:
        print(f"❌ Error durante la población de sectores: {e}")
        raise 