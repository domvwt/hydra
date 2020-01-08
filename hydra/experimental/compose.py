# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from typing import List, Optional

from omegaconf import DictConfig

from hydra._internal.hydra import GlobalHydra, Hydra
from hydra._internal.utils import detect_calling_file_or_module


def initialize(
    config_dir: Optional[str] = None,
    strict: Optional[bool] = None,
    caller_stack_depth: int = 1,
) -> None:
    """
    :param config_dir: config directory relative to the calling script
    :param strict:
    :param caller_stack_depth:
    :return:
    """
    calling_file, calling_module = detect_calling_file_or_module(caller_stack_depth + 1)
    Hydra.create_main_hydra_file_or_module(
        calling_file, calling_module, config_dir, strict
    )


def compose(
    config_file: Optional[str] = None,
    overrides: List[str] = [],
    strict: Optional[bool] = None,
) -> DictConfig:
    """
    :param config_file: optional config file to load
    :param overrides: list of overrides for config file
    :param strict: optionally override the default strict mode
    :return: the composed config
    """
    assert (
        GlobalHydra().is_initialized()
    ), "GlobalHydra is not initialized, use @hydra.main() or call hydra.experimental.initialize() first"

    cfg = GlobalHydra.instance().hydra.compose_config(
        config_file=config_file, overrides=overrides, strict=strict
    )
    assert isinstance(cfg, DictConfig)

    if "hydra" in cfg:
        del cfg["hydra"]
    return cfg