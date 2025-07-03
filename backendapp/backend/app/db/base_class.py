from sqlalchemy.orm import registry

# Create registry
mapper_registry = registry()

# Create declarative base
Base = mapper_registry.generate_base()

# Explicitly configure the registry
mapper_registry.configure()
