/*
 * wep_lcd_ctrl.c
 *
 * Copyright (C) 2003 ETC s.r.o.
 *
 * Simple command line tool for changing contrast and intensity of LCD
 *
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License
 * as published by the Free Software Foundation; either version 2
 * of the License, or (at your option) any later version.
 *
 * Written by Peter Figuli <peposh@etc.sk>, 2003
 *
 */

#include "stdio.h"
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include "wep-ep250.h"
#include <string.h>


static const char *gsm_option = NULL;
static const char *irda_option = NULL;
static const char *gps_option = NULL;
static const char *bcr_option = NULL;
static const char *ess_option = NULL;


static void help( void );
static void gsm( void );
static void irda( void );
static void gps( void );
static void bcr( void );
static void ess( void );

static int fd;

static struct {
  const char *name;
  const char **value;
  const char *description;
  void ( *func)(void );
  int used;
} option[]={
  { "--help", NULL,           "       -displays this help",                 help,      0 },
  { "-gsm",    	&gsm_option, 	"[on/off] -GSM on FFTUART", 	gsm, 1 },
  { "-irda",	&irda_option, 	"[on/off] -IRDA on SSUART", 	irda, 1 },
  { "-gps",    	&gps_option, 	"[on/off] -GPS on STUART",	gps,1 },
  { "-bcr", 	&bcr_option, 	"[on/off] -Bar code reader on SSUART", bcr, 1 },
  { "-ess", 	&ess_option, "[on/off] - Extern SSUART", ess, 1 },
  { NULL,     NULL,           NULL,                                         NULL,      0 }
};

static void help( void ){
  int i;

  printf( "Usage\n" );
  for( i = 0; option[ i ].name != NULL; i++ ){
    printf( "  %s %s\n", option[ i ].name, option[ i ].description );
  }
  printf( "\n\n" );
}

int getValue( const char *value ){
  return !strcmp( value, "on" );
}


static void missing_argument( void ){
  printf( "missing arguemnt 'on' or 'off'\n" );
}

static void gsm( void ){
  if( gsm_option ){
    ioctl( fd,  WEP_CTRL_GSM_IOCTL, getValue( gsm_option ));
  }else{
    missing_argument();
  }
}

static void irda( void ){
  if( irda_option != NULL ){
    ioctl( fd,  WEP_CTRL_IRDA_IOCTL, getValue( irda_option ));
  }else{
    missing_argument();
  }
}

static void gps( void ){
  if( gps_option != NULL ){
    ioctl( fd,  WEP_CTRL_GPS_IOCTL, getValue( gps_option ));
  }else{
    missing_argument();
  }
}
static void bcr( void ){
  if( bcr_option != NULL ){
    ioctl( fd,  WEP_CTRL_BCR_IOCTL, getValue( bcr_option ));
  }else{
    missing_argument();
  }
}
static void ess( void ){
  if( ess_option != NULL ){
    ioctl( fd,  WEP_CTRL_EXTERN_SSUART_IOCTL, getValue( ess_option ));
  }else{
    missing_argument();
  }
}


int
main( int argc, char **argv ){
  int i, used;

  if(( fd = open( "/dev/misc/wepctrl", O_RDONLY )) == -1 ){
    printf( "Unable to open wepctrl driver\n" );
    exit( 1 );
  }

  if( argc > 1 ){
    for( i = 0 ; option[ i ].name; i++ ){
      option[ i ].used = 0;
    }
  }

  while( --argc > 0 ){
    argv++;
    for( i = 0; option[ i ].name != NULL; i++ ){
      if( !strcmp( argv[ 0 ], option[ i ].name )){
	option[ i ].used = 1;
	if( argc > 1 ){
	  if( !strchr( argv[ 1 ], '-' )){
	    argv++; argc--;
	    *option[ i ].value = argv[ 0 ];
	  }
	}
	break;
      }
    } 
  }

  used = 0;
  for( i = 0; option[ i ].name != NULL; i++ ){
    if( option[ i ].used ){
      used++;
      option[ i ].func();
    }
  }
  if( !used ){
    help();
  }
}

