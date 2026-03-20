module spm_chip_sg13cmos5l (
`ifdef USE_POWER_PINS
    inout vdd,
    inout vss,
    inout iovdd,
    inout iovss,
`endif
    inout logic clk,
    inout logic rst_n,
    inout logic x,
    inout logic [15:0] a,
    inout logic y
);

    logic clk_p2c;
    logic rst_p2c;
    logic x_p2c;
    logic [15:0] a_p2c;
    logic y_c2p;

    spm #(.bits(16)) i_spm
    (
        .clk (clk_p2c),
        .rst (rst_p2c),
        .x (x_p2c),
        .a (a_p2c),
        .y (y_c2p)
    );

    (* keep *)
    sg13cmos5l_IOPadVdd vdd_pad  (
        `ifdef USE_POWER_PINS
        .vdd    (vdd),
        .vss    (vss),
        .iovdd  (iovdd),
        .iovss  (iovss)
        `endif
    );

    (* keep *)
    sg13cmos5l_IOPadVss vss_pad  (
        `ifdef USE_POWER_PINS
        .vdd    (vdd),
        .vss    (vss),
        .iovdd  (iovdd),
        .iovss  (iovss)
        `endif
    );

    (* keep *)
    sg13cmos5l_IOPadIOVdd iovdd_pad  (
        `ifdef USE_POWER_PINS
        .vdd    (vdd),
        .vss    (vss),
        .iovdd  (iovdd),
        .iovss  (iovss)
        `endif
    );

    (* keep *)
    sg13cmos5l_IOPadIOVss iovss_pad  (
        `ifdef USE_POWER_PINS
        .vdd    (vdd),
        .vss    (vss),
        .iovdd  (iovdd),
        .iovss  (iovss)
        `endif
    );

    (* keep *)
    sg13cmos5l_IOPadOut30mA y_pad (
        `ifdef USE_POWER_PINS
        .vdd    (vdd),
        .vss    (vss),
        .iovdd  (iovdd),
        .iovss  (iovss),
        `endif
        .c2p    (y_c2p),
        .pad    (y)
    );

    (* keep *)
    sg13cmos5l_IOPadIn clk_pad (
        `ifdef USE_POWER_PINS
        .vdd    (vdd),
        .vss    (vss),
        .iovdd  (iovdd),
        .iovss  (iovss),
        `endif
        .p2c    (clk_p2c),
        .pad    (clk)
    );

    (* keep *)
    sg13cmos5l_IOPadIn rst_pad (
        `ifdef USE_POWER_PINS
        .vdd    (vdd),
        .vss    (vss),
        .iovdd  (iovdd),
        .iovss  (iovss),
        `endif
        .p2c    (rst_p2c),
        .pad    (rst_n)
    );

    (* keep *)
    sg13cmos5l_IOPadIn x_pad (
        `ifdef USE_POWER_PINS
        .vdd    (vdd),
        .vss    (vss),
        .iovdd  (iovdd),
        .iovss  (iovss),
        `endif
        .p2c    (x_p2c),
        .pad    (x)
    );

    genvar a_i;
    generate
        for (a_i = 0; a_i < 16; a_i = a_i + 1) begin : a_pad
            (* keep *)
            sg13cmos5l_IOPadIn i_pad (
                `ifdef USE_POWER_PINS
                .vdd    (vdd),
                .vss    (vss),
                .iovdd  (iovdd),
                .iovss  (iovss),
                `endif
                .p2c    (a_p2c[a_i]),
                .pad    (a[a_i])
            );
        end
    endgenerate

endmodule