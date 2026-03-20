TAG=spm_chip

librelane:
	nix-shell librelane --run "librelane config.yaml --pdk ihp-sg13cmos5l --pdk-root pdk --manual-pdk --overwrite --run-tag $(TAG)"

.PHONY: librelane