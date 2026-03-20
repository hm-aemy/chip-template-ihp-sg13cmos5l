#!/usr/bin/env python3
"""Generate chip top-level SystemVerilog from a YAML description."""

import argparse
import os
import sys

import yaml
from jinja2 import Environment, FileSystemLoader


def power_pad_type(name):
    """Map a power pin name to its pad cell type suffix.

    Examples: iovdd -> IOVdd, iovss -> IOVss, vdd -> Vdd, vss -> Vss
    """
    if name.startswith('io'):
        rest = name[2:]
        return 'IO' + rest[0].upper() + rest[1:]
    return name[0].upper() + name[1:]


def parse_port(port_def):
    """Parse a port definition."""
    if isinstance(port_def, str):
        return {'name': port_def, 'width': 1}
    if isinstance(port_def, dict):
        reserved = {'width', 'map', 'strength'}
        name_keys = [k for k in port_def if k not in reserved]
        if len(name_keys) != 1:
            raise ValueError(f"Expected exactly one signal name key in: {port_def!r}")
        name = name_keys[0]
        port = {'name': name, 'width': port_def.get('width', 1)}
        if 'map' in port_def:
            port['map'] = port_def['map']
        if 'strength' in port_def:
            port['strength'] = port_def['strength']
        return port
    raise ValueError(f"Unknown port definition: {port_def!r}")


def main():
    parser = argparse.ArgumentParser(
        description='Generate chip top-level SystemVerilog from a YAML description'
    )
    parser.add_argument('yaml_file', help='Input YAML file')
    parser.add_argument('-o', '--output', help='Output SV file (default: stdout)')
    parser.add_argument('-f', '--force', action='store_true', help='Overwrite output file if it exists')
    parser.add_argument(
        '-t', '--template-dir',
        help='Directory containing Jinja2 templates (default: script directory)',
        default=os.path.dirname(os.path.abspath(__file__)),
    )
    args = parser.parse_args()

    with open(args.yaml_file) as f:
        cfg = yaml.safe_load(f)

    technology = cfg['technology']   # e.g. ihp-sg13cmos5l
    name = cfg['name']               # e.g. spm_chip_sg13cmos5l

    design_name = cfg['design']

    # Technology prefix for pad cell names: strip leading 'ihp-'
    tech_prefix = technology.removeprefix('ihp-').replace('-', '')  # sg13cmos5l

    # Power pads: name -> count (number of pad instances)
    power_cfg = cfg.get('power', {})
    power = [{'name': k, 'count': v} for k, v in power_cfg.items()]
    power_names = [p['name'] for p in power]
    scalar_power = [p for p in power if p['count'] == 1]
    bus_power = [p for p in power if p['count'] > 1]

    # Parse inputs and outputs
    inputs = []
    for p in cfg.get('inputs', []):
        port = parse_port(p)
        port['signal'] = port.pop('map', port['name'])
        port['dir'] = 'input'
        inputs.append(port)

    outputs = []
    for p in cfg.get('outputs', []):
        port = parse_port(p)
        port['signal'] = port.pop('map', port['name'])
        port['strength'] = port.pop('strength', 30)
        port['dir'] = 'output'
        outputs.append(port)

    all_ports = inputs + outputs

    # Pad cell power pin alignment: pad to max name length + 2
    power_pad_width = max((len(n) for n in power_names), default=0) + 2

    # Separate scalar and bus ports
    scalar_inputs = [inp for inp in inputs if inp['width'] == 1]
    bus_inputs = [inp for inp in inputs if inp['width'] > 1]
    scalar_outputs = [out for out in outputs if out['width'] == 1]
    bus_outputs = [out for out in outputs if out['width'] > 1]

    context = {
        'name': name,
        'technology': technology,
        'tech_prefix': tech_prefix,
        'design_name': design_name,
        'power': power,
        'power_names': power_names,
        'scalar_power': scalar_power,
        'bus_power': bus_power,
        'inputs': inputs,
        'outputs': outputs,
        'all_ports': all_ports,
        'scalar_inputs': scalar_inputs,
        'bus_inputs': bus_inputs,
        'scalar_outputs': scalar_outputs,
        'bus_outputs': bus_outputs,
        'power_pad_width': power_pad_width,
    }

    template_name = 'ihp.sv.jinja2'

    env = Environment(
        loader=FileSystemLoader(args.template_dir),
        keep_trailing_newline=False,
        trim_blocks=True,
        lstrip_blocks=True,
    )
    env.filters['ljust'] = lambda s, w: str(s).ljust(w)
    env.globals['power_pad_type'] = power_pad_type

    template = env.get_template(template_name)
    result = template.render(**context)

    if args.output:
        if os.path.exists(args.output) and not args.force:
            print(f"error: output file '{args.output}' already exists (use -f to overwrite)", file=sys.stderr)
            sys.exit(1)
        with open(args.output, 'w') as f:
            f.write(result)
    else:
        sys.stdout.write(result)


if __name__ == '__main__':
    main()
